from rest_framework import serializers
from children.models import Child
from reports.models import Report
from django.utils import timezone

from children.serializers import ChildrenSerializer


class ReportSerializer(serializers.ModelSerializer):
    child_id = serializers.PrimaryKeyRelatedField(
        source='child',
        queryset=Child.objects.all()
    )

    child = ChildrenSerializer(read_only=True)
    create_at = timezone.now()

    class Meta:
        model = Report
        fields = ('child_id', 'create_at', 'child')


