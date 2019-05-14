from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404

import logging

logger = logging.getLogger('__name__')


def checkResp(request, objtype=''):
    logger.info('Enter: API')

    if request.method == 'POST':
        logger.info('REQUEST POST')

    elif request.method == 'GET':
        logger.info('REQUEST GET')

    else:
        logger.info('REQUEST FAILURE')

    if objtype is None:
        objtype = 'NULL'

    template = loader.get_template('rest.html')
    context = {
        'name': objtype,
    }
    return HttpResponse(template.render(context, request))
