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
        return self.Meta.model(**validated_data)

    # Update method?
    def update(self,instance,validated_data):
        logger.debug('Serializer: UPDATE')
        # Update this to grab whatever fields that exist for the object
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.cat_id = Category.objects.get(pk=validated_data.get('cat_id', instance.cat_id))
        logger.debug('Serializer: RETURNING')
        return instance

class CategorySerializer(serializers.ModelSerializer):
    logger.debug('Enter: {}'.format('CATEGORY SERIALIZER'))
    class Meta:
        model = Category
        fields = '__all__'

    def create(self,validated_data):
        logger.debug('Serializer: CREATE')
        return self.Meta.model(**validated_data)
