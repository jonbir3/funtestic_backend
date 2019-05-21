from rest_framework import serializers
from children.models import Child


class ChildrenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Child
        fields = ('id', 'name',)