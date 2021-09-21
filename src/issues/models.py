from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

class Manager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Vous devez entrer un email')

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,password):
        if not email:
            raise ValueError('Vous devez entrer un email')

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser):
    user_id = models.IntegerField(primary_key=True,unique=True, db_index=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(
        max_length = 100,
        unique=True,
    )
    password = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = Manager()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin


class Issues(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=500)
    tag = models.CharField(max_length=100)
    priority = models.CharField(max_length=10)
    project_id = models.IntegerField()
    status = models.CharField(max_length=10)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name="issue_author")
    assignee_user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name="assignee_user")
    created_time = models.DateTimeField()

class Comments(models.Model):
    comment_id = models.IntegerField()
    description = models.CharField(max_length=500)
    author_user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comment_author')
    issue_id = models.ForeignKey(Issues,on_delete=models.CASCADE,related_name='issues')
    created_time = models.DateTimeField

class Projects(models.Model):
    project_id = models.IntegerField()
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=20)
    author_user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name='author_id')

class Contributors(models.Model):
    user_id = models.IntegerField()
    project_id = models.IntegerField()
    permission = models.CharField(choices=(('A','all'),('N','none')),max_length=10)
    role = models.CharField(max_length=50)
