from rest_framework import serializers
from API.models import Projects
from accounts.models import CustomUser


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    author_user_id = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='id', write_only=True)
    class Meta:
        model = Projects
        fields = ('title','description','type','project_id','author_user_id')
        read_only_fields = ('id',)

    def validate_author(self, value):
        return self.context['request'].user