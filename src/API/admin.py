from django.contrib import admin
from .models import Issues, Comments, Projects, Contributors


class IssueAdmin(admin.ModelAdmin):
    list_display = ['title', 'desc', 'tag', 'priority', 'status',
                    'project_id', 'author_user', 'assignee_user']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'type', 'author_user']


class ContribAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'project_id', 'permission', 'role']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['description', 'author_user', 'issue']


admin.site.register(Issues, IssueAdmin)
admin.site.register(Comments, CommentAdmin)
admin.site.register(Projects, ProjectAdmin)
admin.site.register(Contributors, ContribAdmin)
