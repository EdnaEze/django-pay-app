"""
URL configuration for webapps2023 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from payapp import views
from payapp.views import dashboard as payapp_dash, request_payment, transfer
from register import views as register_views


urlpatterns = [
    path('transfer/', transfer, name='transfer'),
    path('request/', request_payment, name='request'),
    path('dashboard/', payapp_dash, name='dashboard'),
    path('home/', views.home, name='home'),
    path('logout/', register_views.logout_user, name="logout"),
    path('login/', register_views.login_user, name="login"),
    path('register/', register_views.register_user, name="register"),
    path('webapps2023/', views.home, name="home"),
    path('payapp/', include('payapp.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
]
