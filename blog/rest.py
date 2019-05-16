from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Category, Post
from .forms import CatForm, PostForm, LoginForm
from .serializers import CategorySerializer, PostSerializer, BaseSerializer
from rest_framework import viewsets

import logging

# Need to modify this to be a class, rather than just methods

logger = logging.getLogger(__name__)

class PostViewSet(viewsets.ModelViewSet):
    logger.debug('Enter: {}'.format('PostViewSet'))
    queryset = Post.objects.all()
    #serializer_class = PostSerializer
    serializer_class = BaseSerializer('post')

class CategoryViewSet(viewsets.ModelViewSet):
    logger.debug('Enter: {} '.format('CategoryViewSet'))
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
