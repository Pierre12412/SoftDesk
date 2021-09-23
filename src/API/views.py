from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from API.models import *
from API.serializers import RegisterSerializer, ContribSerializer, IssueSerializer
from accounts.models import CustomUser


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


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
        return HttpResponse(status=204)

    elif request.method == 'PUT':
        issue = Issues.objects.filter(project_id=project_id, id=issue_id)
        if issue:
            data = request.data
            serializer = IssueSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({"erreur": "Aucun Problème correspondant"})