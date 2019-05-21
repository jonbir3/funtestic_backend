from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from children.serializers import ChildrenSerializer
from . models import Child


class childList(APIView):

    def get(self, request):
        child = Child.objects.all()
        serializer = ChildrenSerializer(child, many=True)
        return Response(serializer.data)

    def post(self):
        pass
