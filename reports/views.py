from django.db import IntegrityError
from rest_framework import status, exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from children.serializers import ChildrenSerializer
from quiz.models import Quiz
from reports.serializers import ReportSerializer
from users.models import Person
from .models import Child, Report
from cryptography.utils import CbcEngine
from django.utils import timezone

class ReportList(APIView):
    #authentication_classes = (TokenAuthentication,)
    #permission_classes = (IsAuthenticated,)
    def put(self, request):
        try:
            child_id = CbcEngine.get_engine().encrypt(request.data['child_id'])
            child = Child.objects.get(id_number=child_id)
            quiz_of_child = Quiz.objects.filter(child=child)
        except KeyError:
            return Response('child_id field is missing.', status=status.HTTP_400_BAD_REQUEST)
        except Child.DoesNotExist:
            return Response('child does not exist.', status=status.HTTP_400_BAD_REQUEST)
        except Quiz.DoesNotExist:
            return Response('The child has no quiz.', status=status.HTTP_400_BAD_REQUEST)

        request.data['child_id'] = CbcEngine.get_engine().encrypt(request.data['child_id'])

        serializer = ReportSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
        except IntegrityError:
            return Response('The report is already exists', status=status.HTTP_400_BAD_REQUEST)
        return Response('The report added successfully for {} !'.format(child))

# Create your views here.
