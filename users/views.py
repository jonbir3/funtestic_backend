from django.contrib.auth import get_user_model, authenticate
from rest_framework import status, authentication, exceptions
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from cryptography.utils import CbcEngine
from users.serializers import PersonSerializer


class LoginAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):

        # Get the username and password
        username = request.data.get('username', None)
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
        person = serializer.save()
        Token.objects.create(user=person.user)
        return Response('Register successfully!')


class Login(APIView):
    authentication_classes = (LoginAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # TODO: generate password for two factor authentication
        return Response('Login successfully!')


class TwoFA(APIView):
    authentication_classes = (LoginAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # TODO: check if 2fa correct
        is_ok = True
        if not is_ok:
            return Response('Two factor authentication failed.')
        token = Token.objects.get(user=request.user)
        return Response({'token': token.key})
