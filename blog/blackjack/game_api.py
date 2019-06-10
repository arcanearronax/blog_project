from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views import View
from .game_master import BlackJackGame
from .form import BlackJackForm
import logging

logger = logging.getLogger(__name__)

class GameViewSet(View):
    logger.info('Initiating: {}'.format('GameViewset'))

    template = loader.get_template('blackjack/index.html')
    form = BlackJackForm

    print(__name__)

    # Give page to user
    def get(self,request):
        logger.info('Enter: GameViewSet-GET')
        logger.debug('TMP: {}'.format(request.__dict__['session']))

        template = GameViewSet.template
        context = {
            'gameform': GameViewSet.form,
        }
        return HttpResponse(template.render(context,request))

    # Process form submissions and update accordingly
    def post(self,request):
        logger.info('Enter: GameViewSet-POST')
        logger.debug('game_id={}'.format(request.POST.get('game_id')))
        logger.debug('player={}'.format(request.POST.get('player')))
        logger.debug('selection={}'.format(request.POST.get('selection')))
        logger.debug('bet_amount={}'.format(request.POST.get('bet_amount')))

        form = BlackJackForm(request.POST)
        if form.is_valid():
            logger.debug('form is valid')

            # Pull in our attributes
            game = {}
            game['game_id'] = request.POST.get('game_id')
            game['player'] = request.POST.get('player')
            game['selection'] = request.POST.get('selection')
            game['bet_amount'] = request.POST.get('bet_amount')

        else:
            game = {'error': 'Form is invalid'}

        return JsonResponse(game)
