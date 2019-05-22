from rest_framework import serializers
from .models import *
import logging

logger = logging.getLogger('blog.rest')

# All model serializers are based off this class.
class BaseSerializer(serializers.ModelSerializer):
    logger.debug('Enter: {}'.format('Base Serializer'))

    # Subclasses will need to implement a class named Meta

    # Use this to create model instances
    def create(self,validated_data):
        logger.debug('--SerializerCreate:\t{}'.format(validated_data))
        return self.Meta.model(**validated_data).save()

    # Use this to update model instances
    def update(self,instance,validated_data):
        logger.debug('--SerializerUpdate:\t{}'.format(validated_data))

        for k,v in validated_data.items():
            try:
                setattr(instance,k,v)
            except ValueError as v:
                # Just a quick and dirty fix for this for now
                logger.debug('\tV: {}'.format(v))
                try:
                    logger.debug('\tRETRY: {}'.format(k.__class__))
                    setattr(instance,'{}.{}'.format(k,k),v)
                except Exception as e:
                    logger.debug('\tE: {}'.format(e))
            except Exeception as e:
                logger.debug('\tFailure: {}'.format(e))

        # This is required to update the model instance
        instance.save()
        return instance

# Use this for the Post model
class PostSerializer(BaseSerializer):
    logger.debug('Enter: {}'.format('POST SERIALIZER'))

    class Meta:
        model = Post
        fields = '__all__'

class CategorySerializer(BaseSerializer):
    class Meta:
        model = Category
        fields = '__all__'
