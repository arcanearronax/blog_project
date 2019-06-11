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
        logger.debug('game_id={}'.format(request.POST.get('game_id')))
        logger.debug('player={}'.format(request.POST.get('player')))
        logger.debug('selection={}'.format(request.POST.get('selection')))
        logger.debug('bet_amount={}'.format(request.POST.get('bet_amount')))

        form = BlackJackForm(request.POST)
        if form.is_valid():
            logger.debug('Form is valid')

            # Pull in our attributes
            action = {}
            action['game_id'] = request.POST.get('game_id')
            action['player'] = request.POST.get('player')
            action['selection'] = request.POST.get('selection')
            action['bet_amount'] = request.POST.get('bet_amount')
            action['phase'] = request.POST.get('phase')

            # Process game action
            self.game.process_action(action)

        else:
            logger.debug('Form is invalid')
            action = {'error': 'Form is invalid'}

        context = {
            'gameform': GameViewSet.form,
            'game_action': GameAction(request.POST.get('game_id'),request.POST.get('player'),request.POST.get('selection'),request.POST.get('bet_amount'),request.POST.get('game_phase')),
        }

        return HttpResponse(GameViewSet.template.render(context,request))
