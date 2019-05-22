from django.shortcuts import render
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.response import Response
from children.serializers import ChildrenSerializer
from users.models import Person
from . models import Child
from cryptography.utils import CbcEngine


class ChildList(APIView):
    def get(self, request):
        return Response('Forbidden', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            parent_id = CbcEngine.get_engine().decrypt(request.data['id'])
            parent = Person.objects.get(id_number=parent_id)
            children_of_parent = Child.objects.filter(parent=parent)
        except parent.DoesNotExist:
            return Response({'error parent does not exist': self.code_404}, 404)
        except children_of_parent.DoesNotExist :
            return Response({'error child does not exist': self.code_404}, 404)

        serializer = ChildrenSerializer(children_of_parent, many=True)
        return Response(serializer.data)

    def put(self, request):
        parent_id = CbcEngine.get_engine().decrypt(request.data['parent_id'])
        parent = Person.objects.get(id_number=parent_id)

        child_age = CbcEngine.get_engine().encrypt(request.data['age'])
        child_gander = CbcEngine.get_engine().encrypt(request.data['gander'])
        child_name = CbcEngine.get_engine().encrypt(request.data['name'])

        child = Child(parent=parent, name=child_name, gender=child_gander, age=child_age)

        serializer = ChildrenSerializer(child, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request):
    #     parent_id = request.data['parent_id']
    #     parent = Person.objects.get(id_number=parent_id)
    #
    #     cbc_engine = CBC('wwwwwwww', 'qqqqqqqq')
    #
    #     child_age = cbc_engine.encrypt(request.data['child_age'])
    #     child_gander = cbc_engine.encrypt(request.data['child_gander'])
    #     child_name = cbc_engine.encrypt(request.data['child_name'])
    #
    #     child = Child(parent=parent, name=child_name, gender=child_gander, age=child_age)
    #     child.save()
