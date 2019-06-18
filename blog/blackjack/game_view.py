from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views import View
from .game_master import GameMaster
from .form import BlackJackForm
from .game_action import GameAction
from .exceptions import MasterException
import logging

logger = logging.getLogger(__name__)

class GameViewSet(View):
    logger.info('Initiating: {}'.format('GameViewset'))

    template = loader.get_template('blackjack/index.html')
    form = BlackJackForm
    game = GameMaster

    # Give page to user
    def get(self,request):
        logger.info('Enter: GameViewSet-GET')

        template = GameViewSet.template
        context = {
            'gameform': GameViewSet.form,
        }
        return HttpResponse(template.render(context,request))

    # Process form and update info in game
    def post(self,request):
        logger.info('Enter: GameViewSet-POST')

        # Get our vars for processing
        form = BlackJackForm(request.POST)
        action = GameAction()

        # Validate the form
        if form.is_valid():
            logger.debug('Form is valid')

            # Get only the fields GameAction allows
            for key in (key for key in request.POST if key in form.fields):
                GameAction.__setattr__(action,key,request.POST.get(key))

            # Pass the action off to the game
            try:
                self.__class__.game.process_action(action)
            except MasterException as m:
                action.error = m
                action.notes = m

        else:
            logger.debug('Form is invalid')
            action.error = 'Form is invalid'
            action.notes = 'Form is invalid'

        context = {
            'gameform': GameViewSet.form,
            'action': action,
        }

        return HttpResponse(GameViewSet.template.render(context,request))
