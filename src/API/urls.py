from django.urls import path
from API.views import (ProjectsAll, ProjectsDetail, contributor_add,
                       get_issues, update_issue, get_post_comments,
                       put_delete_comments)

urlpatterns = [
    path('api/projects/', ProjectsAll.as_view()),
    path('api/projects/<int:pk>', ProjectsDetail.as_view()),
    path('api/projects/<int:project_id>/users/', contributor_add),
    path('api/projects/<int:project_id>/users/<int:user_id>', contributor_add),
    path('api/projects/<int:project_id>/issues/', get_issues),
    path('api/projects/<int:project_id>/issues/<int:issue_id>', update_issue),
    path('api/projects/<int:project_id>/issues/<int:issue_id>/comments/', get_post_comments),
    path('api/projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>', put_delete_comments),
]
