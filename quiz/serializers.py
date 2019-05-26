from rest_framework import serializers
from quiz.models import Quiz
from children.models import Child
from children.serializers import ChildrenSerializer


class QuizSerializer(serializers.ModelSerializer):
    child_id = serializers.PrimaryKeyRelatedField(
        source='child',
        queryset=Child.objects.all()
    )
    child = ChildrenSerializer(read_only=True)

    class Meta:
        model = Quiz
        fields = ('grade', 'child', 'child_id')

    def to_representation(self, instance):
        self.fields['child'] = ChildrenSerializer(read_only=True)
        return super(QuizSerializer, self).to_representation(instance)

