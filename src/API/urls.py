from django.urls import path
from API.views import (ProjectsAll, ProjectsDetail, contributor_all,
                       get_post_issues, update_delete_get_issue, get_post_comments,
                       put_get_delete_comments)

urlpatterns = [
    path('api/projects/', ProjectsAll.as_view()),
    path('api/projects/<int:pk>', ProjectsDetail.as_view()),
    path('api/projects/<int:project_id>/users/', contributor_all),
    path('api/projects/<int:project_id>/users/<int:user_id>', contributor_all),
    path('api/projects/<int:project_id>/issues/', get_post_issues),
    path('api/projects/<int:project_id>/issues/<int:issue_id>', update_delete_get_issue),
    path('api/projects/<int:project_id>/issues/<int:issue_id>/comments/', get_post_comments),
    path('api/projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>', put_get_delete_comments),
]
