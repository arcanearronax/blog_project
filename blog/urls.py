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
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from rest_framework.authtoken import views as authviews

from . import views, rest, login

urlpatterns = [
    # These are here for legacy support
    # Need to deal with this duplication
    path('', views.BlogView.as_view(), name='blogHome'),
    path('login/', login.BlogLogin.as_view(), name='blogLogin'),
    path('logout/', login.BlogLogout.as_view(), name='blogLogout'),
    path('admin/', views.BlogView.as_view(), name='blogAdmin'),
    re_path(r'^api/', include('blog.router')),
    path('api-auth/',authviews.obtain_auth_token, name="api-auth"),
    path('<slug:desc>/', views.BlogView.as_view(), name='categoryHome'),
	path('<slug:desc>/<int:pk>/', views.BlogView.as_view(), name='blogPost'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
