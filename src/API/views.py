from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from API.serializers import RegisterSerializer
from accounts.models import CustomUser


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer