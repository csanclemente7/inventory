"""inventoryProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)
from inventoryApp import views

urlpatterns = [
    path('login', TokenObtainPairView.as_view()),
    path('refresh', TokenRefreshView.as_view()),
    path('register', views.UserCreateView.as_view()),

    # URLS de usuario
    path('user/<int:pk>', views.UserDetailView.as_view()),

    # URLS de item
    path('item/<int:user>', views.ItemCreateView.as_view()), #ok
    path('item/<int:user>/<int:pk>', views.ItemDetailView.as_view()), #ok
    path('items/<int:user>', views.ItemListView.as_view()), #ok
    path('item/<int:user>/<int:pk>/update', views.ItemUpdateView.as_view()), #ok
    path('item/<int:user>/<int:pk>/delete', views.ItemDeleteView.as_view()), #ok

    # URLS de report
    path('report/<int:user>', views.ReportCreateView.as_view()), #ok
    path('report/<int:user>/<int:pk>', views.ReportDetailView.as_view()), #ok
    path('reports/<int:user>', views.ReportListView.as_view()), #ok
    path('reports/<int:user>/outside', views.ReportOutputListView.as_view()), #ok
    path('report/<int:user>/<int:pk>/update', views.ReportUpdateView.as_view()), #ok
    path('report/<int:user>/<int:pk>/delete', views.ReportDeleteView.as_view()), #ok

]
