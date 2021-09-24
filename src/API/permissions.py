from rest_framework import permissions


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