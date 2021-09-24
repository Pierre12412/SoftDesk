"""SoftDesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from API.views import *
from API.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.obtain_auth_token,name='api-token-auth'),
    path('signup/', RegisterView.as_view(), name='auth_register'),
    path('api/projects/', ProjectsAll.as_view()),
    path('api/projects/<int:pk>', ProjectsDetail.as_view()),
    path('api/projects/<int:project_id>/users/', contributor_add),
    path('api/projects/<int:project_id>/users/<int:user_id>', contributor_add),
    path('api/projects/<int:project_id>/issues/', get_issues),
    path('api/projects/<int:project_id>/issues/<int:issue_id>', update_issue),
    path('api/projects/<int:project_id>/issues/<int:issue_id>/comments/', get_post_comments),
    path('api/projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>', put_delete_comments),
]
