from .models import Category, Post
from .forms import CatForm, PostForm, LoginForm
from .serializers import CategorySerializer, PostSerializer#, BaseSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated

import logging

# Need to modify this to be a class, rather than just methods

logger = logging.getLogger(__name__)

class PostViewSet(viewsets.ModelViewSet):
    logger.debug('Enter: {}'.format('PostViewSet'))
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self,request):
        logger.debug('Enter: {}'.format('getPosts'))
        newest = self.__class__.queryset.order_by('created').last()
        serializer = self.__class__.serializer_class()(newest)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def getPosts(self,request):
        logger.debug('Enter: {}'.format('getPosts'))
        newest = self.get_queryset.order_by('created').last()
        serializer = self.get_serializer_class()(newest)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    logger.debug('Enter: {} '.format('CategoryViewSet'))
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
