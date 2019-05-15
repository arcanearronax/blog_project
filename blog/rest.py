from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Category, Post
from .forms import CatForm, PostForm, LoginForm

import logging

# Need to modify this to be a class, rather than just methods

logger = logging.getLogger(__name__)

def restGet(request, objtype, objind):
    logger.info('Enter: restGet')
    # Getting the obj's queryset
    if objtype:
        try:
            obj = eval('{}.objects.all()'.format(objtype.capitalize()))
            assert obj, 'No objects found'

            if objind:
                obj = obj.filter(pk=objind)
                assert obj, 'Object index not found'

            logger.debug(obj)
            return list(obj.values())
        except Exception as e:
            logger.debug('{} - {}'.format(e.__class__.__name__, e))
    return []


def restReq(request, objtype='',objind=''):
    logger.info('Enter: API - {} - {}'.format(objtype, objind))

    # Need process to validate objtype is a valid model

    if request.method == 'GET':
        obj = restGet(request, objtype, objind)

    elif request.method == 'POST':
        logger.info('REQUEST POST')
        obj = 'POST'

    elif request.method == 'PUT':
        logger.info('REQUEST PUT')
        obj = 'PUT'

    else:
        logger.info('REQUEST FAILURE')
        obj = 'ELSE'

    return JsonResponse(obj, safe=False)
