from rest_framework import serializers
from children.models import Child
from quiz.models import Quiz
from reports.models import Report

from children.serializers import ChildrenSerializer


class ReportSerializer(serializers.ModelSerializer):
    child_id = serializers.PrimaryKeyRelatedField(
        source='child',
        queryset=Child.objects.all()
    )

    child = ChildrenSerializer(read_only=True)
    # quiz = QuizSerializer(read_only=True)

    class Meta:
        model = Report
        fields = ('create_at',)

