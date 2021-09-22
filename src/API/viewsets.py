from API.models import Projects

from .serializers import ProjectSerializer
from rest_framework import viewsets


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer
    def get_queryset(self):
        user = self.request.user
        id = self.request.query_params.get('id')
        if id:
            query = Projects.objects.filter(author_user_id_id=user.id, project_id=id)
        else:
            query = Projects.objects.filter(author_user_id_id=user.id)
        return query