"""
URL configuration for djangoProject project.

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
from django.urls import path, re_path
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('user/getUserInfo/', views.CheckUserInfo.as_view()),
    path('user/register/', views.User_register.as_view()),
    path('user/<str:username>/', views.UserDetailView.as_view()),

    path('bus/getBusInfo/', views.CheckBusInfo.as_view()),
    path('bus/register/', views.Bus_register.as_view()),
    path('bus/<str:b_id>/', views.BusDetailView.as_view()),

    path('ticket/getUserTicketInfo/<str:u_id>/', views.CheckUserTicketInfo.as_view()),
    path('ticket/getBusTicketInfo/<str:b_id>/', views.CheckBusTicketInfo.as_view()),
    path('ticket/register/', views.Ticket_register.as_view()),
    path('ticket/<str:t_id>/', views.TicketDetailView.as_view())

]
