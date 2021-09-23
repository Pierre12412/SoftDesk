from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from API.models import *
from API.serializers import RegisterSerializer, ContribSerializer, IssueSerializer, CommentSerializer, ProjectSerializer
from accounts.models import CustomUser


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

@csrf_exempt
@api_view(["POST","GET","PUT","DELETE"])
def project_get_post(request,project_id=None):
    project = Projects.objects.filter(id=project_id).first()
    if request.method == 'GET':
        if project_id != None:
            if project:
                contributors = Contributors.objects.filter(project_id=project_id)
                contrib_or_user = False
                for contributor in contributors:
                    if contributor.user_id == request.user.id:
                        contrib_or_user = True
                if request.user == project.author_user:
                    contrib_or_user = True
                if contrib_or_user:
                    serializer = ProjectSerializer(project)
                    return Response(serializer.data)
                return JsonResponse({"erreur":"Vous n'avez pas l'authorisation d'accès"},status=401)
            else:
                return JsonResponse({"erreur":"Projet Inexistant"})
        else:
            projects = Projects.objects.all()
            serializer = ProjectSerializer(projects,many=True)
            return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        serializer = ProjectSerializer(data=data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=204)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(["POST","GET","PUT","DELETE"])
def contributor_add(request,project_id,user_id=None):
    if request.method == 'GET':
        contributors = Contributors.objects.filter(project_id=project_id)
        if contributors:
            serializer = ContribSerializer(contributors,many=True)
            return Response(serializer.data)
        else:
            return JsonResponse({"erreur":"Aucun Contributeur"})

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
            return JsonResponse({"erreur":"Aucun Contributeur à supprimer"})
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
def get_issues(request,project_id):
    if request.method == 'GET':
        issues = Issues.objects.filter(project_id=project_id)
        if issues:
            serializer = IssueSerializer(issues,many=True,context={'request': request,'project_id':project_id})
            return Response(serializer.data)
        else:
            return JsonResponse({"erreur":"Aucun Problème"})

    elif request.method == 'POST':
        project = Projects.objects.filter(id=project_id)
        if project:
            data = request.data
            serializer = IssueSerializer(data=data,context={'request': request,'project_id':project_id})
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=204)
            return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({"erreur": "Aucun projet existant avec cet ID"})

@csrf_exempt
@api_view(["DELETE","PUT"])
def update_issue(request,project_id,issue_id):
    if request.method == 'DELETE':
        issue = Issues.objects.filter(project_id=project_id,id=issue_id)
        if issue:
            issue.delete()
        else:
            return JsonResponse({"erreur":"Aucun Problème à supprimer"})
        return JsonResponse({"détail":"Le projet {} a été supprimé".format(issue_id)})

    elif request.method == 'PUT':
        issue = Issues.objects.filter(project_id=project_id, id=issue_id).first()
        if issue:
            data = request.data
            serializer = IssueSerializer(issue,data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({"erreur": "Aucun Problème correspondant"})

@csrf_exempt
@api_view(["GET","POST"])
def get_post_comments(request,project_id,issue_id):
    if existing_issue(project_id,issue_id):
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
    else:
        return JsonResponse({"erreur": 'Projet ou problème inexistant'})

@csrf_exempt
@api_view(["GET","PUT","DELETE"])
def put_delete_comments(request,project_id,issue_id,comment_id):
    if existing_issue(project_id,issue_id):
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

        elif request.method == 'GET':
            comment = Comments.objects.filter(id=comment_id)
            if comment:
                serializer = CommentSerializer(comment,many=True, context={'request': request, 'issue_id': issue_id})
                return Response(serializer.data)
            else:
                return JsonResponse({"erreur": "Aucun Commentaire avec cet ID"})
    else:
        return JsonResponse({"erreur": 'Projet ou problème inexistant'})

def existing_project(project_id):
    project = Projects.objects.filter(id=project_id)
    if project:
        return True
    return False

def existing_issue(project_id,issue_id):
    if not existing_project(project_id):
        return False
    issue = Issues.objects.filter(id=issue_id,project_id=project_id)
    if issue:
        return True
    return False