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
    path('blog/logout/', views.blogLogout, name='blogLogout'),
    path('blog/admin/', views.blogAdmin, name='blogAdmin'),
    path('blog/error/', views.blogError, name='blogError'),
<<<<<<< HEAD
    path('blog/test/', views.blogTest, name='blogTest'),
	path('blog/<slug:desc>/', views.categoryHome, name='categoryHome'),
	path('blog/<slug:cat_desc>/<int:id>/', views.blogPost, name='blogPost'),
=======
    path('blog/<slug:desc>/', views.categoryHome, name='categoryHome'),
	path('blog/<slug:desc>/<int:id>/', views.blogPost, name='blogPost'),

    ############################################
    # Below here is just testing or irrelevant #
    ############################################

    path('blog/test/', views.blogTest, name='blogTest'),
    path('blog/test/<slug:desc>/', views.baseCategory, name='baseCategory'),
    path('blog/test/<slug:desc>/<int:id>/', views.basePage, name='basePage'),
>>>>>>> Updated the templates being used to be less clunky and rearranged a fair bit of the code. Need to work on purging stuff that isnt being used and then fix up the admin page and login functionality.
]
