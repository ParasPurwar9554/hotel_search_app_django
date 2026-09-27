from .views import *
from django.urls import path

urlpatterns = [
   path('',home),
   path('api/get-hotels/',get_hotel)
]