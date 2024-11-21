from django.contrib import admin
from django.urls import path
from home.views import *

urlpatterns = [
    path('submit_register/', SubmitRegister.as_view(), name='submit_register')
]