from .models import Category, Post
from .forms import CatForm, PostForm, LoginForm
from .serializers import CategorySerializer, PostSerializer#, BaseSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .forms import PostForm

import logging

# Need to modify this to be a class, rather than just methods

logger = logging.getLogger(__name__)

class PostViewSet(viewsets.ModelViewSet):
    logger.debug('Enter: {}'.format('PostViewSet'))
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    # GET - post/
    def list(self,request):
        logger.debug('--Get: {}'.format(''))
        serializer = self.get_serializer_class()(self.get_queryset(), many=True)
        return Response(serializer.data)

    # GET - post/{pk}
    def retrieve(self, request, pk=None):
        logger.debug('--Retrieve pk: {}'.format(pk))
        post = get_object_or_404(self.get_queryset(),pk=pk)
        return Response(self.get_serializer_class()(post).data)

    # POST - post/
    def create(self, request):
        logger.debug('--Create: {}'.format(request.data))
        request.data['post_id'] = self.queryset.count() + 1
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            logger.debug('Instance Is Valid')
            instance = serializer.save()
            logger.debug('INSTANCE: {}'.format(instance.__dict__))
            return Response(serializer.data, status=201)
        else:
            logger.debug('Instance Is Invalid')
            return Response(serializer.errors, status=400)

    # PUT - post/{pk}
    def update(self, request, pk=None):
        logger.debug('--Update: {}'.format(pk))
        try:
            post = get_object_or_404(self.get_queryset(),pk=pk)
        except Error as e:
            logger.debug('ERROR: {}'.format(e))
            return Response(e, status=503)

        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
        #instance = serializer.update(post,request.data)
            instance = serializer.update(instance=post,validated_data=request.data)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

    # This is just for custom methods
    # @action(methods=['get'], detail=False)
    # def getPost(self,request):
    #     logger.debug('Enter: {}'.format('method: getPost'))
    #     newest = self.get_queryset().order_by('pub_date').last()
    #     serializer = self.get_serializer_class()(newest)
    #     return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    logger.debug('Enter: {} '.format('CategoryViewSet'))
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
