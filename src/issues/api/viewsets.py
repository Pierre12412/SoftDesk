from issues.models import Projects
from .serializers import ProjectSerializer
from rest_framework import viewsets

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer