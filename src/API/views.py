from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from API.models import Projects, Contributors, Comments, Issues
from API.permissions import IsAuthorOrReadOnly
from API.serializers import RegisterSerializer, ContribSerializer, IssueSerializer, CommentSerializer, ProjectSerializer
from accounts.models import CustomUser
from API.permissions import author_permission, contributor_author_permission


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


@api_view(["POST","GET","PUT","DELETE"])
@permission_classes([IsAuthenticated])
def contributor_all(request,project_id,user_id=None):

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
            return JsonResponse({"erreur":"Aucun Collaborateur ?? supprimer"})
        return HttpResponse(status=204)

    elif request.method == 'POST':
        data = request.data
        serializer = ContribSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=204)
        return JsonResponse(serializer.errors, status=400)


@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def get_post_issues(request,project_id):

    if not contributor_author_permission(request,project_id):
        return JsonResponse({"erreur": "Vous n'avez pas l'autorisation"})

    get_object_or_404(Projects, id=project_id)

    if request.method == 'GET':
        issues = Issues.objects.filter(project_id=project_id)
        if issues:
            serializer = IssueSerializer(issues,many=True,context={'request': request,'project_id':project_id})
            return Response(serializer.data)
        else:
            return JsonResponse({"erreur":"Aucun Probl??me"})

    elif request.method == 'POST':
        data = request.data
        serializer = IssueSerializer(data=data,context={'request': request,'project_id':project_id})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=204)
        return JsonResponse(serializer.errors, status=400)


@api_view(["DELETE","PUT","GET"])
@permission_classes([IsAuthenticated])
def update_delete_get_issue(request,project_id,issue_id):

    issue = get_object_or_404(Issues, id=issue_id)

    if not contributor_author_permission(request,project_id):
        return JsonResponse({"erreur": "Vous n'avez pas l'autorisation"})

    if request.method == "GET":
        if issue:
            serializer = IssueSerializer(issue)
            return Response(serializer.data)
        return JsonResponse({"erreur": "Aucun probl??me existant avec cet ID"})

    if not author_permission(request, issue) :
        return JsonResponse({"erreur": "Vous n'avez pas l'autorisation"})

    if request.method == 'DELETE':
        issue = Issues.objects.filter(project_id=project_id,id=issue_id)
        if issue:
            issue.delete()
        else:
            return JsonResponse({"erreur":"Aucun Probl??me ?? supprimer"})
        return JsonResponse({"d??tail":"Le probl??me {} a ??t?? supprim??".format(issue_id)})

    elif request.method == 'PUT':
        data = request.data
        serializer = IssueSerializer(issue,data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


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
            return JsonResponse({"erreur": "Aucun probl??me existant avec cet ID"})


@api_view(["GET","PUT","DELETE"])
@permission_classes([IsAuthenticated])
def put_get_delete_comments(request,project_id,issue_id,comment_id):

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
            return JsonResponse({"erreur": "Aucun Commentaire ?? supprimer"})
        return JsonResponse({"d??tail": "Le commentaire {} a ??t?? supprim??".format(comment_id)})

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

