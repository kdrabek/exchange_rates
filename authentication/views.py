from django.contrib.auth import authenticate
from django.utils.six import BytesIO


from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from authentication.models import User


def get_json(request):
    stream = BytesIO(request.body)
    return JSONParser().parse(stream)


class LoginView(APIView):

    def post(self, request):
        data = get_json(request)
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return Response(
                {'error': 'Password or email is missing'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(email=email, password=password)
        if user is not None:
            token = Token.objects.get(user=user.id)
            return Response(
                {'token': token.key},
                status=status.HTTP_200_OK
            )

        return Response(
            {'error': 'Could not authenticate using provided credentials'},
            status=status.HTTP_400_BAD_REQUEST
        )


class RegisterView(APIView):

    def post(self, request):
        data = get_json(request)
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return Response(
                {'error': 'Password or email is missing'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(email=email, password=password)
            token = Token.objects.get(user=user.id)

            return Response(
                {'user': user.id, 'token': token.key},
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                {'error': 'User already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )
