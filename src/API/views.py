from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from API.models import *
from API.permissions import IsAuthorOrReadOnly
from API.serializers import RegisterSerializer, ContribSerializer, IssueSerializer, CommentSerializer, ProjectSerializer
from accounts.models import CustomUser


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ProjectsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthorOrReadOnly]


class ProjectsAll(generics.ListCreateAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer


def existing_comment(project_id,issue_id,comment_id):
    get_object_or_404(Projects, id=project_id)
    get_object_or_404(Issues, id=issue_id)
    comment = Comments.objects.filter(id=comment_id)
    if comment:
        return True
    return False

def author_permission(request,obj):
    if obj is None:
        return False
    if request.user.id == obj.author_user_id:
        return True
    return False


def contributor_author_permission(request,project_id):
    if author_permission(request,Projects.objects.filter(id=project_id).first()):
        return True
    contributors = Contributors.objects.filter(project_id=project_id)
    for contributor in contributors:
        if contributor.user_id == request.user.id:
            return True
    return False



@csrf_exempt
@api_view(["POST","GET","PUT","DELETE"])
@permission_classes([IsAuthenticated])
def contributor_add(request,project_id,user_id=None):

    get_object_or_404(Projects, id=project_id)

    if not author_permission(request,Projects.objects.filter(id=project_id).first()):
        return JsonResponse({"erreur": "Vous n'avez pas l'autorisation"})

    if request.method == 'GET':
        contributors = Contributors.objects.filter(project_id=project_id)
        if contributors:
            serializer = ContribSerializer(contributors,many=True)
            return Response(serializer.data)
        else:
            return JsonResponse({"erreur":"Aucun Collaborateur"})

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ContribSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        contributor = Contributors.objects.filter(project_id=project_id,user_id=user_id)
        if contributor:
            contributor.delete()
        else:
            return JsonResponse({"erreur":"Aucun Collaborateur à supprimer"})
        return HttpResponse(status=204)

    elif request.method == 'POST':
        data = request.data
        serializer = ContribSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=204)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def get_issues(request,project_id):

    if not contributor_author_permission(request,project_id):
        return JsonResponse({"erreur": "Vous n'avez pas l'autorisation"})

    get_object_or_404(Projects, id=project_id)

    if request.method == 'GET':
        issues = Issues.objects.filter(project_id=project_id)
        if issues:
            serializer = IssueSerializer(issues,many=True,context={'request': request,'project_id':project_id})
            return Response(serializer.data)
        else:
            return JsonResponse({"erreur":"Aucun Problème"})

    elif request.method == 'POST':
        data = request.data
        serializer = IssueSerializer(data=data,context={'request': request,'project_id':project_id})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=204)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(["DELETE","PUT","GET"])
@permission_classes([IsAuthenticated])
def update_issue(request,project_id,issue_id):

    issue = get_object_or_404(Issues, id=issue_id)

    if not contributor_author_permission(request,project_id):
        return JsonResponse({"erreur": "Vous n'avez pas l'autorisation"})

    if request.method == "GET":
        if issue:
            serializer = IssueSerializer(issue)
            return Response(serializer.data)
        return JsonResponse({"erreur": "Aucun problème existant avec cet ID"})

    if not author_permission(request, issue) :
        return JsonResponse({"erreur": "Vous n'avez pas l'autorisation"})

    if request.method == 'DELETE':
        issue = Issues.objects.filter(project_id=project_id,id=issue_id)
        if issue:
            issue.delete()
        else:
            return JsonResponse({"erreur":"Aucun Problème à supprimer"})
        return JsonResponse({"détail":"Le problème {} a été supprimé".format(issue_id)})

    elif request.method == 'PUT':
        data = request.data
        serializer = IssueSerializer(issue,data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def get_post_comments(request,project_id,issue_id):

    get_object_or_404(Issues, id=issue_id)

    if not contributor_author_permission(request,project_id):
        return JsonResponse({"erreur": "Vous n'avez pas l'autorisation"})

    if request.method == 'GET':
        comments = Comments.objects.filter(issue_id=issue_id)
        if comments:
            serializer = CommentSerializer(comments,many=True,context={'request': request,'issue_id':issue_id})
            return Response(serializer.data)
        else:
            return JsonResponse({"erreur":"Aucun Commentaire"})

    elif request.method == 'POST':
        issue = Issues.objects.filter(id=issue_id)
        if issue:
            data = request.data
            serializer = CommentSerializer(data=data, context={'request': request, 'issue_id': issue_id})
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=204)
            return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({"erreur": "Aucun problème existant avec cet ID"})


@csrf_exempt
@api_view(["GET","PUT","DELETE"])
@permission_classes([IsAuthenticated])
def put_delete_comments(request,project_id,issue_id,comment_id):

    comment = get_object_or_404(Comments, id=comment_id)

    if request.method != 'GET':
        if not author_permission(request,comment):
            return JsonResponse({"erreur": "Vous n'avez pas l'autorisation"})

    if request.method == 'GET':
        if not contributor_author_permission(request, project_id):
            return JsonResponse({"erreur": "Vous n'avez pas l'autorisation"})
        if comment:
            serializer = CommentSerializer(comment, context={'request': request, 'issue_id': issue_id})
            return Response(serializer.data)
        else:
            return JsonResponse({"erreur": "Aucun Commentaire avec cet ID"})

    get_object_or_404(Issues, id=issue_id)
    if request.method == 'DELETE':
        comment = Comments.objects.filter(id=comment_id)
        if comment:
            comment.delete()
        else:
            return JsonResponse({"erreur": "Aucun Commentaire à supprimer"})
        return JsonResponse({"détail": "Le commentaire {} a été supprimé".format(comment_id)})

    elif request.method == 'PUT':
        comment = Comments.objects.filter(id=comment_id).first()
        if comment:
            data = request.data
            serializer = CommentSerializer(comment, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({"erreur": "Aucun Commentaire correspondant"})

