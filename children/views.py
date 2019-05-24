from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from children.serializers import ChildrenSerializer
from users.models import Person
from . models import Child
from cryptography.utils import CbcEngine


class ChildList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            parent_id = CbcEngine.get_engine().encrypt(request.data['id'])
            parent = Person.objects.get(phone_number=parent_id)
            children_of_parent = Child.objects.filter(parent=parent)
        except KeyError:
            return Response('id field is missing.', status=status.HTTP_400_BAD_REQUEST)
        except parent.DoesNotExist:
            return Response('Parent does not exist.', status=status.HTTP_400_BAD_REQUEST)
        except children_of_parent.DoesNotExist:
            return Response('The parent has no children.', status=status.HTTP_400_BAD_REQUEST)

        serializer = ChildrenSerializer(children_of_parent, many=True)
        return Response(serializer.data)

    def put(self, request):
        parent_id = CbcEngine.get_engine().encrypt(request.data['parent_id'])
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
