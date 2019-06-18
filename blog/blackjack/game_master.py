from .objects.card_deck import PlayingCardDeck
from .objects.player import BlackJackPlayer, BlackJackDealer
from .game import BlackJackGame
from .exceptions import GameException,MasterException
from .game_action import GameAction
import logging

logger = logging.getLogger('blog.blackjack.game_view')

# May want to end up having this extend dict
class GameMaster():
    _game_class = BlackJackGame
    games = dict()

    # Simply add a new game object to the games dict
    @classmethod
    def create_game(cls,action):
        try:
            game_id = str(int(action.game_id))
            cls.games[game_id] = cls._game_class()
        except Exception as e:
            action.error = 'e'
        else:
            action.notes = 'Game created successfully'

        return action

    @classmethod
    def create_player(cls,action):
        try:
            game_id = str(int(action.game_id))
            game = cls.games[game_id]
            game.add_player(action.player_name,action.chips)
        except Exception as e:
            action.add_error(e)
        else:
            action.add_note('Player created for game: {}'.format(game_id))

    @classmethod
    def start_round(cls,action):
        logger.debug('ENTER: start_round')
        try:
            game_id = str(int(action.game_id))
            game = cls.games[game_id]
            player_name = action.player_name
            game.add_bet(player_name,action.chips)
            game.deal_initial_hand()
            action.hands = game.get_player(player_name).get_hands()
            game.set_available_moves(player_name)
        except Exception as e:
            action.add_error(e)
        else:
            action.hands = game.get_cards(player_name)
            logger.debug('GOT CARDS: {}'.format(action.hands))
            action.add_note('Cards dealt to: {}'.format(player_name))

    @classmethod
    def player_move(cls,action):
        game_id = str(int(action.game_id))
        game = cls.games[game_id]
        player_name = action.player_name

        try:
            game.process_move(player_name,action.move)
        except Exception as e:
            action.hands = game.get_cards(player_name)
            action.error = e
            action.notes = e
        else:
            action.hands = game.get_cards(player_name)

    _phase_router = {
        'create_game': create_game,
        'create_player': create_player,
        'start_round': start_round,
        'player_move': player_move,
    }

    #######################
    ## Action Processing ##
    #######################

    # Use this to comunicate with the view set
    @classmethod
    def process_action(cls,action):
        logger.debug('PROCESS ACTION: {}'.format(action.__dict__))

        if action.phase in cls._phase_router:
            eval('cls.{}(action)'.format(action.phase))
        else:
            action.notes = 'ACTION NOT FOUND'

        return action
