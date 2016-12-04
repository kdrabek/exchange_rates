from django.conf.urls import url
from django.contrib import admin

from authentication.views import LoginView, LogoutView, RegisterView


urlpatterns = [
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    url(r'^register$', RegisterView.as_view(), name='register'),
]
