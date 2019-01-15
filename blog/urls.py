"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path

from . import views

urlpatterns = [
    # Need to figure out 'overloading paths' here to make this work
    path('blog/', views.blogHome, name='blogHome'),
    path('blog/login/', views.blogLogin, name='blogLogin'),
    path('blog/admin/', views.blogAdmin, name='blogAdmin'),
    path('blog/error/', views.blogError, name='blogError'),
    path('blog/home/', views.blogHome, name='blogHome'),
	path('blog/<slug:desc>/', views.categoryHome, name='categoryHome'),
    path('blog/<slug:cat_desc>/admin', views.categoryAdmin, name='categoryAdmin'),
	path('blog/<slug:cat_desc>/<int:id>/', views.blogPost, name='blogPost'),
]
