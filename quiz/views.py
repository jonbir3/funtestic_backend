from rest_framework.views import APIView
from quiz.serializers import QuizSerializer
from rest_framework.response import Response
from cryptography.utils import CbcEngine
from children.models import Child
from rest_framework import status, exceptions
from django.db import IntegrityError
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class SaveChildGrade(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        try:
            child_id = CbcEngine.get_engine().encrypt(request.data['child_id'])
            child = Child.objects.get(id_number=child_id)
            parent = child.parent
            if parent.user.username != request.user.username:
                raise exceptions.AuthenticationFailed(detail='Not authorized request.')
        except KeyError:
            return Response('One of the fields are missing.', status=status.HTTP_400_BAD_REQUEST)
        except Child.DoesNotExist:
            return Response('child does not exist.', status=status.HTTP_400_BAD_REQUEST)

        request.data['child_id'] = child_id
        serializer = QuizSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
        except IntegrityError:
            return Response('Quiz is already exists', status=status.HTTP_400_BAD_REQUEST)
        return Response('Quiz added successfully!')
