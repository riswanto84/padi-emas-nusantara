from django.urls import path
from .views import landing_page, dashboard, season_list, season_create, season_close, user_list, user_create, user_edit, weather_forecast
from finance.views import season_report

urlpatterns = [
    path('', landing_page, name='landing'),
    path('dashboard/', dashboard, name='dashboard'),
    path('api/cuaca/', weather_forecast, name='weather_forecast'),
    path('musim-tanam/', season_list, name='season_list'),
    path('musim-tanam/mulai/', season_create, name='season_create'),
    path('musim-tanam/<int:pk>/tutup/', season_close, name='season_close'),
    path('musim-tanam/<int:pk>/laporan/', season_report, name='season_report'),
    path('pengguna/', user_list, name='user_list'),
    path('pengguna/tambah/', user_create, name='user_create'),
    path('pengguna/<int:pk>/ubah/', user_edit, name='user_edit'),
]
