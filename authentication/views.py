import json

from django.shortcuts import render_to_response, redirect
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View
from django.template import RequestContext

from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response

from authentication.models import User


class LoginView(APIView):

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return HttpResponseBadRequest(
                json.dumps({'error': 'Password or email is missing'})
            )

        user = authenticate(email=email, password=password)
        if user is not None:
            return HttpResponse(
                json.dumps({'result': 'Success'})
            )
            # generate JWT
        return HttpResponse(
            json.dumps({'oops': 'something went wrong', 'user': user})
        )


class RegisterView(APIView):

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return HttpResponseBadRequest(
                json.dumps({'error': 'Password or email is missing'})
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(email=email, password=password)
            return HttpResponse(
                json.dumps({'user': user.id})
            )
            # generate JWT
        else:
            return HttpResponseBadRequest(
                json.dumps({'error': 'User already exists.'})
            )
