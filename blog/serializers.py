from rest_framework import serializers
import logging
from .models import *

logger = logging.getLogger('blog.rest')

class PostSerializer(serializers.ModelSerializer):
    logger.debug('Enter: {}'.format('POST SERIALIZER'))

    class Meta:
        model = Post
        fields = '__all__'

    def create(self,validated_data):
        logger.debug('Serializer: CREATE')
        logger.debug('VALIDATED: {}'.format(validated_data))
        return self.Meta.model(**validated_data)

    # Update method?

class CategorySerializer(serializers.ModelSerializer):
    logger.debug('Enter: {}'.format('CATEGORY SERIALIZER'))
    class Meta:
        model = Category
        fields = '__all__'
