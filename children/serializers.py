from rest_framework import serializers
from children.models import Child
from users.models import Person
from users.serializers import PersonSerializer


class ChildrenSerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(
        source='parent',
        queryset=Person.objects.all()
    )
    parent = PersonSerializer(read_only=True)

    class Meta:
        model = Child
        fields = ('id_number', 'name', 'age', 'gender', 'parent', 'parent_id')

    def to_representation(self, instance):
        self.fields['parent'] = PersonSerializer(read_only=True)
        return super(ChildrenSerializer, self).to_representation(instance)
