from rest_framework import serializers
from .models import *
import logging

logger = logging.getLogger('blog.rest')

class BaseSerializer(serializers.ModelSerializer):
    logger.debug('Enter: {}'.format('Base Serializer'))

    # Investigate using class methods to dynamically create serializers

    def create(self,validated_data):
        logger.debug('{}: Create'.format(self.__class__.__name__))
        return self.Meta.model(**validated_data)

    def update(self,instance,validated_data):
        logger.debug('{}: Update'.format(self.__class__.__name__))

        for k,v in validated_data.items():
            logger.debug('{}:\t{}'.format(k,v))
            try:
                setattr(instance,k,v)
            except ValueError as v:
                # Just a quick and dirty fix for this for now
                logger.debug(v)
                setattr(instance,'{}.{}'.format(k,k),v)
            except Exeception as e:
                logger.debug('Failure: {}'.format(e))

        instance.save()

class PostSerializer(BaseSerializer):
    logger.debug('Enter: {}'.format('POST SERIALIZER'))

    class Meta:
        model = Post
        fields = '__all__'


    # Update method?
    # def update(self,instance,validated_data):
    #     logger.debug('Serializer: UPDATE')
    #     # Update this to grab whatever fields that exist for the object
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.text = validated_data.get('text', instance.text)
    #     instance.cat_id = Category.objects.get(pk=validated_data.get('cat_id', instance.cat_id))
    #     logger.debug('Serializer: RETURNING')
    #     return instance

# class PostSerializer(serializers.ModelSerializer):
#     logger.debug('Enter: {}'.format('POST SERIALIZER'))
#
#     class Meta:
#         model = Post
#         fields = '__all__'
#
#     def create(self,validated_data):
#         logger.debug('Serializer: CREATE')
#         return self.Meta.model(**validated_data)
#
#     # Update method?
#     def update(self,instance,validated_data):
#         logger.debug('Serializer: UPDATE')
#         # Update this to grab whatever fields that exist for the object
#         instance.title = validated_data.get('title', instance.title)
#         instance.text = validated_data.get('text', instance.text)
#         instance.cat_id = Category.objects.get(pk=validated_data.get('cat_id', instance.cat_id))
#         logger.debug('Serializer: RETURNING')
#         return instance

class CategorySerializer(BaseSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# class CategorySerializer(serializers.ModelSerializer):
#     logger.debug('Enter: {}'.format('CATEGORY SERIALIZER'))
#     class Meta:
#         model = Category
#         fields = '__all__'
#
#     def create(self,validated_data):
#         logger.debug('Serializer: CREATE')
#         return self.Meta.model(**validated_data)
#
#     def update(self,instance,validated_data):
#         logger.debug('Serializer: UPDATE')
#         instance.desc = validated_data.get('desc', instance.desc)
#         instance.hide = validated_data.get('hide', instance.hide)
#         logger.debug('Serializer: RETURNING')
#         return instance
