from rest_framework import serializers
import logging
from .models import *

logger = logging.getLogger('blog.rest')

class BaseSerializer(serializers.ModelSerializer):
    logger.debug('Enter: {}'.format('BASE SERIALIZER'))

class CategorySerializer(serializers.ModelSerializer):
    logger.debug('Enter1: {}'.format('CATEGORY SERIALIZER'))
    class Meta:
        model = Category
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    logger.debug('Enter2: {}'.format('POST SERIALIZER'))
    class Meta:
        model = Post
        fields = '__all__'
