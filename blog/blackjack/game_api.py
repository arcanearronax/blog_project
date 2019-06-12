from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views import View
from .game_master import BlackJackGame
from .form import BlackJackForm
from .game_action import GameAction
import logging

logger = logging.getLogger(__name__)

class GameViewSet(View):
    logger.info('Initiating: {}'.format('GameViewset'))

    template = loader.get_template('blackjack/index.html')
    form = BlackJackForm
    game = BlackJackGame(1000)

    # Give page to user
    def get(self,request):
        logger.info('Enter: GameViewSet-GET')
        logger.debug('TMP: {}'.format(request.__dict__['session']))

        template = GameViewSet.template
        context = {
            'gameform': GameViewSet.form,
        }
        return HttpResponse(template.render(context,request))

    # Process form and update info in game
    def post(self,request):
        logger.info('Enter: GameViewSet-POST')

        form = BlackJackForm(request.POST)
        action = GameAction()
        if form.is_valid():
            logger.debug('Form is valid')

            # Pull in our attributes
            action.game_id = request.POST.get('game_id')
            action.player = request.POST.get('player')
            action.selection = request.POST.get('selection')
            action.bet_amount = request.POST.get('bet_amount')
            action.phase = request.POST.get('phase')

            # Process game action
            self.game.process_action(action)

        else:
            logger.debug('Form is invalid')
            action.error = 'Form is invalid'

        context = {
            'gameform': GameViewSet.form,
            'game_action': action,
        }

        return HttpResponse(GameViewSet.template.render(context,request))
