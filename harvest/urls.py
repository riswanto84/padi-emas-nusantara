from django.urls import path
from .views import harvest_list
urlpatterns=[path('',harvest_list,name='harvest_list')]
