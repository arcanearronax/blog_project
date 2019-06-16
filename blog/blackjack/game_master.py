from .objects.card_deck import PlayingCardDeck
from .objects.player import BlackJackPlayer, BlackJackDealer
from .game import BlackJackGame
from .exceptions import GameException
from .game_action import GameAction
import logging

logger = logging.getLogger('blog.blackjack.game_api')

class GameMaster():
    _game_class = BlackJackGame
    games = dict()

    ###################
    ## Phase Routing ##
    ###################

    # Simply add a new game object to the games dict
    @classmethod
    def create_game(cls,action):
        try:
            id = str(int(action.game_id))
        except Exception as e:
            action.error = 'e'
        else:
            cls.games[str(id)] = cls._game_class()

        return action

    @classmethod
    def create_player(cls,action):
        try:
            player = cls._game_class._player_class(action.player,action.chips)
            cls.games[action.game_id].add_player(player)
        except Exception as e:
            logger.error('Some error: {}'.format(e))

    @classmethod
    def place_bet(cls,action):
        logger.debug('Enter: place_bet')
        self.add_bet(action.player,action.chips)

    @classmethod
    def deal_cards(cls,action):
        logger.debug('Enter: deal_cards')
        cls.games[action.game_id].add_card(action.player)
        cls.games[action.game_id].dealer.add_card(hidden=True)
        cls.games[action.game_id].add_card(action.player)
        cls.games[action.game_id].dealer.add_card()

    _phase_router = {
        'create_game': create_game,
        'create_player': create_player,
        'place_bet': place_bet,
        'deal_cards': deal_cards,
        #'player_move': player_move,
    }

    #######################
    ## Action Processing ##
    #######################

    # Use this to comunicate with the API
    @classmethod
    def process_action(cls,action):
        logger.debug('PROCESS ACTION: {}'.format(action.__dict__))

        cls._phase_router[action.phase](cls,action)

        return action
