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
from . models import Child
from cryptography.utils import CbcEngine
# from django.core.mail import EmailMessage


class ReportList(APIView):
    #authentication_classes = (TokenAuthentication,)
    #permission_classes = (IsAuthenticated,)
    def put(self, request):
        try:
            child_id = CbcEngine.get_engine().encrypt(request.data['child_id'])
            child = Child.objects.get(phone_number=child_id)
            if child.user.username != request.user.username:
                raise exceptions.AuthenticationFailed(detail='Not authorized request.')
            quiz_of_child = Quiz.objects.filter(child_id=child_id)
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
        return Response('The report added successfully!')


# class SendReportToEmail(APIView):
#
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#
#     def put(self, request):
#         try:
#             child_id = CbcEngine.get_engine().encrypt(request.data['child_id'])
#             child = Child.objects.get(id_number=child_id)
#             parent = child.parent
#             if parent.user.username != request.user.username:
#                 raise exceptions.AuthenticationFailed(detail='Not authorized request.')
#         except KeyError:
#             return Response('One of the fields are missing.', status=status.HTTP_400_BAD_REQUEST)
#         except Child.DoesNotExist:
#             return Response('child does not exist.', status=status.HTTP_400_BAD_REQUEST)
#
#         parent_email = parent.user.email
#         report = 'media/reports/test.pdf'
#         email = EmailMessage(
#             'report for child', 'Here is the message.', 'from@me.com', [parent_email])
#         email.attach_file(report)
#         email.send()
#         return Response('Report send successfully!')

