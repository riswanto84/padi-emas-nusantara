from django.urls import path
from .views import sale_list
urlpatterns=[path('',sale_list,name='sale_list')]
