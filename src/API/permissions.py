from rest_framework import permissions

from API.models import Projects, Contributors


class IsAuthorOrReadOnly(permissions.BasePermission):
    message = "Vous n'êtes pas l'auteur, vous n'avez pas l'autorisation"

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return request.user.id == obj.author_user_id


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