from rest_framework import serializers
import logging
from .models import *

logger = logging.getLogger('blog.rest')

# class BaseSerializer(serializers.ModelSerializer):
#     logger.debug('Enter: {}'.format('BASE SERIALIZER'))
#
#     class Meta:
#         model = None
#         fields = '__all__'
#
#     def get_queryset(self):
#          model = self.kwargs.get('model')
#          logger.debug('QUERYSET: {}'.format(model))
#          return model.objects.all()
#
#     def get_serializer_class(self):
#         logger.debug('SERIALIZER_CLASS: {}'.format(1))
#         BaseSerializer.Meta.model = self.kwargs.get('model')
#         return BaseSerializer

class PostSerializer(serializers.ModelSerializer):
    logger.debug('Enter2: {}'.format('POST SERIALIZER'))
    class Meta:
        model = Post
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    logger.debug('Enter1: {}'.format('CATEGORY SERIALIZER'))
    class Meta:
        model = Category
        fields = '__all__'
