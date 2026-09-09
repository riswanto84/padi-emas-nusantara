from django.urls import path, include

urlpatterns=[
    path('login/',include('accounts.urls')),
    path('',include('core.urls')),
    path('pengeluaran/',include('finance.urls')),
    path('panen/',include('harvest.urls')),
    path('penjualan/',include('sales.urls')),
]
