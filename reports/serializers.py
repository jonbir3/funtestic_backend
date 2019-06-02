from rest_framework import serializers
from children.models import Child
from reports.models import Report

from children.serializers import ChildrenSerializer


class ReportSerializer(serializers.ModelSerializer):
    child_id = serializers.PrimaryKeyRelatedField(
        source='child',
        queryset=Child.objects.all()
    )

    child = ChildrenSerializer(read_only=True)

    class Meta:
        model = Report
        fields = ('child_id', 'create_at', 'child')


