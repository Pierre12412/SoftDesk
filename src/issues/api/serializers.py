from rest_framework import serializers
from issues.models import Projects

class ProjectSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Projects
        fields = ('title','description','author_user_id')