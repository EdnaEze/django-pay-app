from django.urls import path
from .views import ConversionView

urlpatterns = [
    path('conversion/<str:currency1>/<str:currency2>/<str:amount_of_currency1>/', ConversionView.as_view(),
         name='conversion'),
]
