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
        game = cls.games[action.game_id]
        game.add_player(action.player_name,action.chips)

    @classmethod
    def start_round(cls,action):
        game = cls.games[action.game_id]
        player_name = action.player_name
        game.add_bet(player_name,action.chips)
        game.deal_initial_hand()
        action.hands = game.get_player(player_name).get_hands()

    @classmethod
    def player_move(cls,action):
        game = cls.games[action.game_id]
        player_name = action.player_name
        try:
            game.process_move(player_name,action.move)
        except GameException as e:
            action.error = e
            action.notes = 'Move not allowed?'

    _phase_router = {
        'create_game': create_game,
        'create_player': create_player,
        'start_round': start_round,
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
