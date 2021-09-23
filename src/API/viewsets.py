from API.models import Projects, Contributors

from .serializers import ProjectSerializer
from rest_framework import viewsets


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.user
        id = self.request.query_params.get('id')
        if id:
            query = Projects.objects.filter(author_user_id=user.id, id=id)
        else:
            query = Projects.objects.filter(author_user_id=user.id)
        contributor = Contributors.objects.filter(user_id=user.id)
        projects = []
        for project in contributor:
            projects.append(Projects.objects.filter(id=project.project_id))

        for project in projects:
            query = query | project

        return query