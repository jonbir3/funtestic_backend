from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from children.serializers import ChildrenSerializer
from users.models import Person
from . models import Child


class ChildList(APIView):

    def post(self, request):
        parent_id = request.data['id']
        parent = Person.objects.get(id_number=parent_id)

        children_of_parent = Child.objects.filter(parent=parent)

        serializer = ChildrenSerializer(children_of_parent, many=True)
        return Response(serializer.data)

    def put(self, request):
        parent_id = request.data['parent_id']
        parent = Person.objects.get(id_number=parent_id)

        child_id = request.data['child_id']
        child_age = request.data['child_age']
        child_gander = request.data['child_gander']
        child_name = request.data['child_name']