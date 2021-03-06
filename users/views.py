from django.contrib.auth import get_user_model, authenticate
from django.db import IntegrityError
from rest_framework import status, authentication, exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from cryptography.utils import CbcEngine
from users.models import Person
from users.serializers import PersonSerializer
from random import randint
from users.models import TwoFactorAuthentication
from utilities.send_mail import send_mail
from smtplib import SMTPRecipientsRefused


class LoginAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):

        # Get the username and password
        username = request.data.get('phone_number', None)
        password = request.data.get('password', None)

        if not username or not password:
            raise exceptions.AuthenticationFailed(detail='No credentials provided.')

        username = CbcEngine.get_engine().encrypt(username)

        credentials = {
            get_user_model().USERNAME_FIELD: username,
            'password': password
        }

        user = authenticate(**credentials)

        if user is None:
            raise exceptions.AuthenticationFailed(detail='Invalid username/password.')

        if not user.is_active:
            raise exceptions.AuthenticationFailed(detail='User inactive or deleted.')

        return user, None  # authentication successful


class Register(APIView):

    def put(self, request):
        serializer = PersonSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            person = serializer.save()
        except IntegrityError as e:
            print(e)
            return Response('The user is already exists', status=status.HTTP_400_BAD_REQUEST)
        Token.objects.create(user=person.user)
        return Response('Register successfully!')


class Login(APIView):
    authentication_classes = (LoginAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        random_password = str(randint(100000, 999999))
        login_user = request.user

        try:
            TwoFactorAuthentication.objects.get(user=request.user).delete()
        except TwoFactorAuthentication.DoesNotExist as e:
            print(e)

        two_fa = TwoFactorAuthentication(user=login_user, code_to_verification=random_password)
        try:
            two_fa.save()
        except IntegrityError as e:
            print(e)
            return Response('{0} (probably you try to login twice sequentially)'.format(e),
                            status=status.HTTP_400_BAD_REQUEST)

        user_email_to_send = CbcEngine.get_engine().decrypt(login_user.email)
        subject = 'Verification Code - Funtestic'
        body = 'Hi, in order to login into Funtestic App - Please use the following security code: ' + \
               random_password
        try:
            send_mail(subject, body, user_email_to_send)
        except SMTPRecipientsRefused:
            two_fa.delete()
            raise exceptions.AuthenticationFailed(detail='Invalid email address.')
        return Response('Login successfully!')


class TwoFA(APIView):
    authentication_classes = (LoginAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        code_verification_to_check = CbcEngine.get_engine().encrypt(request.data['2fa_pass'])
        try:
            two_fa = TwoFactorAuthentication.objects.get(user=request.user)
        except TwoFactorAuthentication.DoesNotExist as e:
            return Response('{0} (probably you try to do 2fa twice sequentially)'.format(e),
                            status=status.HTTP_400_BAD_REQUEST)
        code_verification = two_fa.code_to_verification
        if code_verification_to_check != code_verification:
            raise exceptions.AuthenticationFailed(detail='Two factor authentication failed.')
        two_fa.delete()
        token = Token.objects.get(user=request.user)
        return Response({'token': token.key})


class ParentDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            phone_number = CbcEngine.get_engine().encrypt(request.data['phone_number'])
            parent = Person.objects.get(phone_number=phone_number)
            if parent.user.username != request.user.username:
                raise exceptions.AuthenticationFailed(detail='Not authorized request.')
        except KeyError:
            return Response('id_number field is missing.', status=status.HTTP_400_BAD_REQUEST)
        except Person.DoesNotExist:
            return Response('Parent does not exist.', status=status.HTTP_400_BAD_REQUEST)

        serializer = PersonSerializer(parent, read_only=True)
        serializer.data['user'].pop('password')
        return Response(CbcEngine.get_engine().decrypt_parent_json(serializer.data))
