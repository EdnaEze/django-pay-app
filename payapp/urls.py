from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('transfer/', views.transfer, name='transfer'),
    path('request-payment/', views.request_payment, name='request_payment'),
    path('admin/', views.admin_view, name='admin_view'),
]
