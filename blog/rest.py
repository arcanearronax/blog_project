from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Category, Post
from .forms import CatForm, PostForm, LoginForm
from .serializers import CategorySerializer, PostSerializer
from rest_framework import viewsets

import logging

# Need to modify this to be a class, rather than just methods

logger = logging.getLogger(__name__)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    logger.debug(serializer_class.__class__.__name__)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
