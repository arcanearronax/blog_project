from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Category, Post
from .forms import CatForm, PostForm, LoginForm
from .serializers import CategorySerializer, PostSerializer, BaseSerializer
import logging

logger = logging.getLogger(__name__)

class BaseViewSet(viewsets.ModelViewSet):
    logger.debug('Enter: {}'.format('Base Viewset'))

    class Tmp:
        model = None

    # logger.debug('Check Model:')
    # if (Tmp.model):
    #     logger.debug('Model Exists')
    #     serializer_class = eval('{}Serializer'.format(Tmp.model))
    #     queryset = serializer_class.Meta.model.objects.all()
    authentication_classes = (TokenAuthentication,SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    # GET
    def list(self,request):
        logger.debug('--List:\t{}'.format(request.body))
        serializer = self.get_serializer_class()(self.get_queryset(), many=True)
        return Response(serializer.data)

    # GET /pk
    def retrieve(self,request,pk=None):
        logger.debug('--List:\t{}'.format(request.body))
        # I think there needs to be a serializer method to call for this
        instance = get_object_or_404(self.get_queryset(),pk=pk)
        return Response(self.get_serializer_class()(instance).data)

    # POST
    def create(self,request):
        logger.debug('--Create:\t{}'.format(request.body))
        request.data['post_id'] = self.queryset.count() + 1
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            obj = self.get_serializer_class().Meta.model
            logger.debug('\t--OBJ: {}'.format(obj.__dict__))
            for k in serializer.data:
                logger.debug('\t--{}:'.format(k))
                eval('obj.set_{}(serializer.data["{}"])'.format(k,k))

            serializer.save()
            return Response(serializer.data, status=201)
        else:
            logger.debug('Instance Is Invalid')
            logger.debug(serializer.errors)
            return Response(serializer.errors, status=400)

    # PUT - /{pk}
    def update(self, request, pk=None):
        logger.debug('--ViewUpdate:\t{}'.format(pk))

        # Get the model instance or...
        try:
            instance = self.get_serializer_class().Meta.model.objects.get(pk=pk)
            logger.debug('\t--Instance Class: {}'.format(instance.__class__))

        # Pass along to create()
        except Exception as e:
            logger.debug('\t--Instance Exception: {}'.format(e))
            self.create(request)

        # Get our serializer with request data
        request.data['post_id'] = pk
        for k,v in request.data.items():
            logger.debug('\t--TEST: {} -\t{}'.format(k,v))
        serializer = self.get_serializer_class()(data=request.data,partial=True)
        logger.debug('\t--Serializer Data: {}'.format(serializer))

        # Validate our serializer
        if (serializer.is_valid()):
            logger.debug('\t--Serializer is valid')

            # Update the instance based on the request data
            instance = serializer.update(instance=instance,validated_data=request.data)
            logger.debug('\t--TESTER: {}'.format(instance.__class__))
            serializer.save()

            # Return the instance we updated
            logger.debug('\t--Return2')
            return Response(serializer.data, status=201)

        # Serializer is invalid
        else:
            # Return an error
            logger.debug('\tSerializer is invalid')
            logger.debug(serializer.errors)
            logger.debug(serializer.data)
            return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        logger.debug('--Destroy: {}'.format(pk))
        try:
            post = self.get_serializer_class().Meta.objects.get(pk=pk).delete()
        except TypeError as t:
            logger.debug('\tInstance does not exist: {}'.format(pk))
            return Response({'warning': 'pk does not exist: {}'.format(pk)})
        except Exception as e:
            logger.debug('\tDestroy Error: {}'.format(e))
            return Response({'error': e}, status=500)
        else:
            return Response({'post_id': pk}, status=200)

class PostViewSet(BaseViewSet):
    logger.debug('Enter: {}'.format('PostViewSet'))

    class Tmp:
        model = Post

    serializer_class = eval('{}Serializer'.format(Tmp.model.__name__))
    queryset = serializer_class.Meta.model.objects.all()

# class PostViewSet(viewsets.ModelViewSet):
#     logger.debug('Enter: {}'.format('PostViewSet'))
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     authentication_classes = (TokenAuthentication,SessionAuthentication,)
#     permission_classes = (IsAuthenticated,)
#
#     # GET - post/
#     def list(self,request):
#         logger.debug('--List: {}'.format('posts'))
#
#         serializer = self.get_serializer_class()(self.get_queryset(), many=True)
#         return Response(serializer.data)
#
#     # GET - post/{pk}
#     def retrieve(self, request, pk=None):
#         logger.debug('--Retrieve pk: {}'.format(pk))
#         post = get_object_or_404(self.get_queryset(),pk=pk)
#         return Response(self.get_serializer_class()(post).data)
#
#     # POST - post/
#     def create(self, request):
#         logger.debug('--Create: {}'.format(request.data))
#         request.data['post_id'] = self.queryset.count() + 1
#         serializer = self.get_serializer_class()(data=request.data)
#         if serializer.is_valid():
#             logger.debug('Instance Is Valid')
#             instance = serializer.save()
#             instance.save()
#             logger.debug('INSTANCE: {}'.format(instance.__dict__))
#             return Response(serializer.data, status=201)
#         else:
#             logger.debug('Instance Is Invalid')
#             logger.debug(serializer.errors)
#             return Response(serializer.errors, status=400)
#
#     # PUT - post/{pk}
#     def update(self, request, pk=None):
#         logger.debug('--Update: {}'.format(pk))
#         try:
#             post = Post.objects.get(pk=pk)
#         except Exception as e:
#             logger.debug(e)
#             return self.create(request)
#         serializer = self.get_serializer_class()(data=request.data,partial=True)
#         if serializer.is_valid():
#             instance = serializer.update(instance=post,validated_data=request.data)
#             serializer.save()
#             return self.retrieve(request,pk=pk)
#         else:
#             logger.debug('SERIALIZER: {}'.format('invalid'))
#             logger.debug(serializer.errors)
#             return Response(serializer.errors, status=400)
#
#     def destroy(self, request, pk=None):
#         logger.debug('--Destroy: {}'.format(pk))
#         try:
#             post = Post.objects.get(pk=pk).delete()
#         except TypeError as t:
#             logger.debug('Post does not exist: {}'.format(pk))
#             return Response({'warning': 'pk does not exist: {}'.format(pk)})
#         except Exception as e:
#             logger.debug('Destroy Error: {}'.format(e))
#             return Response({'error': e}, status=500)
#         else:
#             return Response({'post_id': pk}, status=200)

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
        logger.debug('--Update: {}'.format(pk))

        # Get existing object or create new record
        try:
            category = Category.objects.get(pk=pk)
        except Exception as e:
            logger.debug(e)
            return self.create(request)

        # Open our serializer
        serializer = self.get_serializer_class()(data=request.data,partial=True)

        # Check if serializer is valuid
        if serializer.is_valid():
            logger.debug('SERIALIZER: {}'.format('valid'))

            # update the instance
            instance = serializer.update(instance=category,validated_data=request.data)
            logger.debug('INSTANCE: {}'.format(instance))

            # Save the serializer
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            logger.debug('SERIALIZER INVALID: {}'.format(serializer.errors))
            return Response(serializer.errors, status=400)

    def destroy(self,request,pk=None):
        logger.debug('--Destroy: {}'.format(pk))
        try:
            post = Category.objects.get(pk=pk).delete()
        except TypeError as t:
            logger.debug('Post does not exist: {}'.format(pk))
            return Response({'warning': 'pk does not exist: {}'.format(pk)})
        except Exception as e:
            logger.debug('Destroy Error: {}'.format(e))
            return Response({'error': e}, status=500)
        else:
            return Response({'cat_id': pk}, status=200)
