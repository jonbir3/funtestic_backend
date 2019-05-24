from django.db import IntegrityError
from rest_framework import status, exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from children.serializers import ChildrenSerializer
from users.models import Person
from . models import Child
from cryptography.utils import CbcEngine


class AddChild(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        try:
            phone_number = CbcEngine.get_engine().encrypt(request.data['parent_id'])
            parent = Person.objects.get(phone_number=phone_number)
            if parent.user.username != request.user.username:
                raise exceptions.AuthenticationFailed(detail='Not authorized request.')
        except KeyError:
            return Response('One of the fields are missing.', status=status.HTTP_400_BAD_REQUEST)
        except Person.DoesNotExist:
            return Response('parent does not exist.', status=status.HTTP_400_BAD_REQUEST)

        request.data['parent_id'] = CbcEngine.get_engine().encrypt(request.data['parent_id'])
        serializer = ChildrenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
        except IntegrityError:
            return Response('The child is already exists', status=status.HTTP_400_BAD_REQUEST)
        return Response('The child added successfully!')


class ChildList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            phone_number = CbcEngine.get_engine().encrypt(request.data['parent_id'])
            parent = Person.objects.get(phone_number=phone_number)
            if parent.user.username != request.user.username:
                raise exceptions.AuthenticationFailed(detail='Not authorized request.')
            children_of_parent = Child.objects.filter(parent_id=phone_number)
        except KeyError:
            return Response('parent_id field is missing.', status=status.HTTP_400_BAD_REQUEST)
        except Person.DoesNotExist:
            return Response('Parent does not exist.', status=status.HTTP_400_BAD_REQUEST)
        except Child.DoesNotExist:
            return Response('The parent has no children.', status=status.HTTP_400_BAD_REQUEST)

        serializer = ChildrenSerializer(children_of_parent, many=True, read_only=True)
        children_list = []
        for child in serializer.data:
            child['parent']['user'].pop('password')
            children_list.append(CbcEngine.get_engine().decrypt_child_json(child))
        return Response(children_list)


class ChildDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            id_number = CbcEngine.get_engine().encrypt(request.data['id_number'])
            child = Child.objects.get(id_number=id_number)
            parent_username = child.parent.user.username
            if parent_username != request.user.username:
                raise exceptions.AuthenticationFailed(detail='Not authorized request.')
        except KeyError:
            return Response('id_number field is missing.', status=status.HTTP_400_BAD_REQUEST)
        except Person.DoesNotExist:
            return Response('Parent does not exist.', status=status.HTTP_400_BAD_REQUEST)
        except Child.DoesNotExist:
            return Response('The child not exist.', status=status.HTTP_400_BAD_REQUEST)

        serializer = ChildrenSerializer(child, read_only=True)
        serializer.data['parent']['user'].pop('password')
        return Response(CbcEngine.get_engine().decrypt_child_json(serializer.data))
