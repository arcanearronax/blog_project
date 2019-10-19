from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Category, Post
from blog.forms import CatForm, PostForm, LoginForm
from blog.serializers import CategorySerializer, PostSerializer, BaseSerializer
from rest_framework.exceptions import APIException
import logging

logger = logging.getLogger(__name__)

class BaseViewSet(viewsets.ModelViewSet):
    logger.info('Initiating: {}'.format('Base Viewset'))

    class Tmp:
        model = None

    authentication_classes = (TokenAuthentication,SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    # Use this to get the model instance with the primary key
    def getObject(self,pk):
        try:
            return self.Tmp.model.objects.get(pk=pk)
        except Exception as e:
            logger.error('error: {}'.format(e))
            raise APIException('Object not found: {}'.format(pk))


    # GET (all objects)
    # Not seeing an update in Github
    def list(self,request):
        logger.info('List')
        return Response(self.get_serializer_class()(self.get_queryset(), many=True).data, status=200)

    # GET (single object) /{pk}
    def retrieve(self,request,pk=None):
        logger.info('Retrieve:\t{}'.format(pk))
        try:
            return Response(self.get_serializer_class()(self.getObject(pk)).data)
        except APIException as a:
            return Response('Object not found: {}'.format(pk),status=404)
        except Exception as e:
            logger.error('{}'.format(e))
            return Response('Unknown Server Error',status=500)

    # POST
    def create(self,request):
        logger.info('Create:\t{}'.format(request.data))

        # Add a primary key ID entry to get a valid
        req_data = request.data
        req_data[self.Tmp.model._meta.pk.name] = self.get_queryset().count() + 1
        logger.debug('request_data: {}'.format(req_data))

        # Validate the serializer and save the instance or fail
        serializer = self.get_serializer_class()(data=req_data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                logger.error(e)
                return Response('Object Not Saved',status=500)
            return Response(serializer.data, status=201)
        else:
            logger.debug('error: {}'.format(serializer.errors))
            return Response('Invalid Request', status=400)

        return Response('Unknown Issue', status=500)

    # PUT /{pk}
    def update(self, request, pk=None):
        logger.info('Update:\t{}'.format(pk))

        # Get the model instance or try to create the object
        try:
            instance = self.getObject(pk=pk)
            logger.debug('primary key found')
        except Exception as e:
            logger.debug('primary key not found')
            logger.error(self.Tmp.model._meta.pk)
            request.data[self.Tmp.model._meta.pk] = pk
            return self.create(request)

        # Pull request data
        req_data = request.data
        logger.debug('request_data: {}'.format(req_data))

        # Update the instance with the request data
        # Need validation here...
        try:
            serializer = self.get_serializer_class()(data=req_data)
            instance = serializer.update(instance,req_data)
            instance.save()
        except Exception as e:
            logger.debug('error: {}'.format(e))
            return Response('Object Not Updated',status=500)

        return Response(self.get_serializer_class()(instance).data, status=202)

    # delete /{pk}
    def destroy(self, request, pk=None):
        logger.info('Destroy: {}'.format(pk))

        # Delete object or fail
        try:
            instance = self.getObject(pk=pk)
            instance.delete()
            return Response(self.get_serializer_class()(instance).data, status=200)
        except APIException as a:
            logger.error(a)
            return Response('Object not found',status=404)
        except Exception as e:
            logger.error('error: {}'.format(e))
            return Response('Request failure', status=500)

class PostViewSet(BaseViewSet):
    logger.info('Initiating: {}'.format('PostViewSet'))

    class Tmp:
        model = Post

    serializer_class = eval('{}Serializer'.format(Tmp.model.__name__))
    queryset = serializer_class.Meta.model.objects.all()

class CategoryViewSet(BaseViewSet):
    logger.info('Initiating: {} '.format('CategoryViewSet'))

    class Tmp:
        model = Category

    serializer_class = eval('{}Serializer'.format(Tmp.model.__name__))
    queryset = serializer_class.Meta.model.objects.all()
