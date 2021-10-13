from django.db import models

from accounts.models import CustomUser
from django.shortcuts import get_object_or_404

# Create your models here.


class Issues(models.Model):
    title = models.CharField(max_length=100, verbose_name='Titre')
    desc = models.CharField(max_length=200, verbose_name='Description')
    tag = models.CharField(max_length=100, verbose_name='Tag')
    priority = models.CharField(max_length=10, verbose_name='Priorité')
    status = models.CharField(max_length=10, verbose_name='Status')
    project_id = models.IntegerField(verbose_name='Identifiant Projet')
    author_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="issue_author", verbose_name='Auteur')
    assignee_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="assignee_user", verbose_name='Utilisateur assigné')
    created_time = models.DateTimeField(verbose_name='Date de création', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Issues'

    def __str__(self):
        return self.title


class Comments(models.Model):
    description = models.CharField(max_length=200)
    author_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='comment_author', verbose_name='Auteur')
    issue = models.ForeignKey(Issues,on_delete=models.CASCADE,related_name='issues',verbose_name= 'Problème')
    created_time = models.DateTimeField(verbose_name='Date de Création', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.description


class Projects(models.Model):
    title = models.CharField(max_length=20, verbose_name='Titre')
    description = models.CharField(max_length=200)
    type = models.CharField(max_length=20)
    author_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='author_id', verbose_name='Auteur')

    class Meta:
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.title


class Contributors(models.Model):
    user_id = models.IntegerField(verbose_name='ID Contributeur')
    project_id = models.IntegerField(verbose_name='ID du Projet')
    permission = models.CharField(choices=(('A','all'),('N','none')),max_length=10, verbose_name='Permissions')
    role = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Contributors'

    def __str__(self):
        user = get_object_or_404(CustomUser, id=self.user_id)
        return user.email
