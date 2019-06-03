from rest_framework import serializers
from children.models import Child
from reports.models import Report

from children.serializers import ChildrenSerializer


class ReportSerializer(serializers.ModelSerializer):
    id_number = serializers.PrimaryKeyRelatedField(
        source='child',
        queryset=Child.objects.all()
    )

    child = ChildrenSerializer(read_only=True)

    class Meta:
        model = Report
        fields = ('id_number', 'create_at', 'child')


