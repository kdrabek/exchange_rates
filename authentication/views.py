from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.template import RequestContext
from django.contrib.auth import login as django_login, authenticate, logout as django_logout

from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response

from authentication.models import User
# from authentication.serializers import UserSerializer


class LoginView(APIView):

    def post(self, request):
        pass


class LogoutView(APIView):

    def post(self, request):
        pass


class RegisterView(APIView):

    def get(self, request):
        users = User.objects.all()
        #serializers = UserSerializer(users, many=True)
        return Response({'serializer.data': 'xx'})

    def post(self, request):
        return HttpResponse(request.POST)
