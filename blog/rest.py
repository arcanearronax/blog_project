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
            instance.save()
            logger.debug('INSTANCE: {}'.format(instance.__dict__))
            return Response(serializer.data, status=201)
        else:
            logger.debug('Instance Is Invalid')
            return Response(serializer.errors, status=400)

    # PUT - post/{pk}
    def update(self, request, pk=None):
        logger.debug('--Update: {}'.format(pk))
        post = Post.objects.get(pk=pk)
        serializer = self.get_serializer_class()(data=request.data,partial=True)
        if serializer.is_valid():
            logger.debug('SERIALIZER: {}'.format('valid'))
            instance = serializer.update(instance=post,validated_data=request.data)
            logger.debug('INSTANCE: {}'.format(instance))
            # I feel like there should be a better way to handle this
            instance.save()
            serializer.save()
            # The above should also address this
            return self.retrieve(request,pk=pk)
        else:
            logger.debug('SERIALIZER: {}'.format('invalid'))
            logger.debug(serializer.errors)
            return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        logger.debug('--Destroy: {}'.format(pk))
        try:
            post = Post.objects.get(pk=pk).delete()
        except TypeError as t:
            logger.debug('Post does not exist: {}'.format(pk))
            return Response({'warning': 'pk does not exist: {}'.format(pk)})
        except Exception as e:
            logger.debug('Destroy Error: {}'.format(e))
            return Response({'error': e}, status=500)
        else:
            return Response({'post_id': pk}, status=200)

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
    authentication_classes = (TokenAuthentication,SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self,request):
        logger.debug('--Get: {}'.format(''))
        serializer = self.get_serializer_class()(self.get_queryset(), many=True)
        return Response(serializer.data)

    def retrieve(self,request,pk=None):
        logger.debug('--Retrieve pk: {}'.format(pk))
        post = get_object_or_404(self.get_queryset(),pk=pk)
        return Response(self.get_serializer_class()(post).data)

    def create(self,request):
        logger.debug('--Create: {}'.format(request.data))
        request.data['cat_id'] = self.queryset.count() + 1
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            logger.debug('Instance Is Valid')
            instance = serializer.save()
            instance.save()
            logger.debug('INSTANCE: {}'.format(instance.__dict__))
            return Response(serializer.data, status=201)
        else:
            logger.debug('Instance Is Invalid')
            return Response(serializer.errors, status=400)

    def update(self,request,pk=None):
        raise NotImplementedError('To do')

    def destroy(self,request,pk=None):
        raise NotImplementedError('To do')
