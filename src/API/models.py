from django.db import models
from rest_framework.generics import get_object_or_404

from accounts.models import CustomUser

# Create your models here.

class Issues(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=500)
    tag = models.CharField(max_length=100)
    priority = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    project_id = models.IntegerField()
    author_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="issue_author")
    assignee_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="assignee_user")
    created_time = models.DateTimeField()

class Comments(models.Model):
    description = models.CharField(max_length=500)
    author_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='comment_author')
    issue = models.ForeignKey(Issues,on_delete=models.CASCADE,related_name='issues')
    created_time = models.DateTimeField

class Projects(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=20)
    author_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='author_id')


class Contributors(models.Model):
    user_id = models.IntegerField()
    project_id = models.IntegerField()
    permission = models.CharField(choices=(('A','all'),('N','none')),max_length=10)
    role = models.CharField(max_length=50)