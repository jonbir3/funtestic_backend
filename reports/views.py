from django.db import IntegrityError
from rest_framework import status, exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from quiz.models import Quiz
from reports.serializers import ReportSerializer
from utilities.send_mail import send_mail
from .models import Child
from cryptography.utils import CbcEngine
import fpdf


class ReportList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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

            # ___write report to text___:
            # text_file = open("media/{}_report.txt".format(child), "w")
            # text_file.write("report:\nname: {0}\nage: {1}\ncreated Date: {2}\ngrades: "
            #                 .format(child, CbcEngine.get_engine().decrypt(child.age), serializer.data['create_at']))
            # i = 0
            # for q in quiz_of_child:
            #     if i + 1 == len(quiz_of_child):
            #         text_file.write("{0} ".format(CbcEngine.get_engine().decrypt(q.grade)))
            #     else:
            #         text_file.write("{0}, ".format(CbcEngine.get_engine().decrypt(q.grade)))
            #         i += 1
            # text_file.close()

            # ____write report to pdf___:
            pdf = fpdf.FPDF(format='letter')
            pdf.add_page()
            pdf.set_font("Arial", "BU", size=24)
            pdf.set_text_color(0, 0, 128)

            pdf.write(5, "report:\n\n")

            pdf.set_font("Arial", size=12)
            pdf.set_text_color(0, 0, 0)
            pdf.write(5, "name: {0}\nage: {1}\ncreated Date: {2}\ngrades: "
                      .format(child, CbcEngine.get_engine().decrypt(child.age), (CbcEngine.get_engine().decrypt(serializer.data['create_at'])).split(' ')[0]))

            i = 0
            for q in quiz_of_child:
                if i + 1 == len(quiz_of_child):
                    pdf.write(5, "{0} ".format(CbcEngine.get_engine().decrypt(q.grade)))
                else:
                    pdf.write(5, "{0}, ".format(CbcEngine.get_engine().decrypt(q.grade)))
                i += 1

            pdf_name = "{}_report.pdf".format(child)
            subject = 'Report for child - Funtestic'
            body = 'Hi! We sent you a report for your child.'
            pdf.output("media/{}".format(pdf_name))
            # ___________________________

            # print( "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            # print(subject)
            # print(body)
            # #print(child.parent.email)
            # print(pdf_name)
            #
            # user = Child.objects.get(id=child.parent.id)
            # print(user)

            send_mail(subject, body, CbcEngine.get_engine().decrypt(child.parent.user.email), pdf_name)
        except IntegrityError:
            return Response("The report is already exists", status=status.HTTP_400_BAD_REQUEST)
        return Response('The report added successfully!')
