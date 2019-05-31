from rest_framework import serializers
from .models import *
import logging

logger = logging.getLogger('blog.rest')

# All model serializers are based off this class.
class BaseSerializer(serializers.ModelSerializer):
    logger.info('Initiating: {}'.format('Base Serializer'))

    # Subclasses will need to implement a class named Meta

    # Use this to create model instances
    def create(self,validated_data):
        logger.info('\tcreate: {}'.format(validated_data))

        obj = self.Meta.model(**validated_data)
        obj.save()
        return obj

    # Use this to update model instances
    def update(self,instance,validated_data):
        logger.info('\tupdate: {}'.format(instance))

        for k,v in validated_data.items():
            if k != '_state':
                logger.debug('\t{}: {}'.format(k,v))
                try:
                    instance.__dict__[k] = v
                except Exception as e:
                    logger.debug(e)

        return instance


# Use this for the Post model
class PostSerializer(BaseSerializer):
    logger.debug('Initiating: {}'.format('Post Serializer'))

    class Meta:
        model = Post
        fields = '__all__'
        id_name = 'post_id'

class CategorySerializer(BaseSerializer):
    logger.debug('Initiating: {}'.format('CategorySerializer'))
    class Meta:
        model = Category
        fields = '__all__'
        id_name = 'cat_id'
