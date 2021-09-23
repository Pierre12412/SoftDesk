from datetime import datetime

from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.validators import UniqueValidator

from API.models import Projects, Contributors, Issues, Comments
from accounts.models import CustomUser


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('title','description','type','author_user','id')


class ContribSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributors
        fields = ('user_id','project_id','permission','role')


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = ('id','title','desc','tag','priority','status','assignee_user')

    def create(self, validated_data):
        user = self.context.get("request").user
        project = self.context.get("project_id")
        issue = Issues(**validated_data)
        issue.created_time = datetime.now()
        issue.author_user = user
        issue.project_id = project
        issue.save()
        return issue

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('description','issue_id','id')

    def create(self, validated_data):
        user = self.context.get("request").user
        issue = self.context.get("issue_id")
        comment = Comments(**validated_data)
        comment.issue_id = issue
        comment.author_user = user
        comment.save()
        return comment

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password2')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
        )
        try:
            if validated_data['first_name']:
                user.first_name = validated_data['first_name']
            if validated_data['last_name']:
                user.first_name = validated_data['last_name']
        except:
            pass

        user.set_password(validated_data['password'])
        user.save()

        return user