from .game import BlackJackGame
from .game_action import GameAction
from .game_response import GameResponse
from .exceptions import GameException,MasterException
import logging

logger = logging.getLogger('blog.blackjack.game_view')

# May want to end up having this extend dict
class GameMaster():
    _game_class = BlackJackGame
    games = dict()

    def get_response(game,action):
        logger.debug('ENTER: get_response')

        resp = GameResponse()
        resp.game_id = action.game_id
        try:
            logger.debug('get_response - test1')
            player_name = game.get_player(action.player_name).get_name()
            resp.player_name = player_name
            player = game.get_player(player_name)
            resp.chip_count = player.get_chips()
        except Exception:
            return resp
        else:
            try:
                logger.debug('get_response - test2')
                resp.bet_amount = game.get_bet(player_name)
                logger.debug('get_response - test2.1')
                resp.player_score = player.get_score()
                logger.debug('get_response - test2.2')
                resp.player_hand = player.get_hand()
                resp.dealer_hand = game.ger_dealer().get_hand()
            except Exception as e:
                logger.debug('RESPONSE ERROR: {}'.format(e))
                return resp

            if game.game_done:
                try:
                    logger.debug('get_response - test3')
                    resp.dealer_score = game.get_dealer().get_score()
                except Exception:
                    return resp
                else:
                    if game.is_simple_winner(player_name):
                        resp.result = '{} wins'.format(player_name)
                    else:
                        resp.result = '{} loses'.format(player_name)
                    resp.reason = '{} vs {}'.format(player.get_score(),game.dealer.get_score())
            return resp

    # Simply add a new game object to the games dict
    @classmethod
    def create_game(cls,action):
        logger.debug('ENTER: create_game')
        game_id = str(int(action.game_id))
        try:
            cls.games[game_id] = cls._game_class()
        except Exception as e:
            loggger.debug('create_game_error: {}'.format(e))
            action.error = 'e'
        else:
            success = 'Created Game {}'.format(game_id)
            logger.debug('create_game: {}'.format(success))
            action.add_note(success)

    @classmethod
    def create_player(cls,action):
        logger.debug('ENTER: create_player')
        game_id = str(int(action.game_id))
        try:
            game = cls.games[game_id]
            game.add_player(action.player_name,action.chips)
        except Exception as e:
            loggger.debug('create_player_error: {}'.format(e))
            action.add_error(e)
        else:
            success = '{} added to game {}'.format(action.player_name,game_id)
            logger.debug('create_player: {}'.format(success))
            action.add_note(success)

    @classmethod
    def start_round(cls,action):
        logger.debug('ENTER: start_round')
        game_id = str(int(action.game_id))
        try:
            game = cls.games[game_id]
            player_name = game.get_player(action.player_name).get_name()
            game.add_bet(player_name,action.chips)
            game.deal_initial_hand()
        except Exception as e:
            logger.debug('start_round_error: {}'.format(e))
            action.add_error(e)
        else:
            action.dealer_hand = game.get_dealer_cards()
            action.hands = game.get_cards(player_name)

            success = '{} dealt: {}'.format(player_name,action.hands)
            logger.debug('start_round: {}'.format(success))
            action.add_note(success)

    @classmethod
    def player_move(cls,action):
        logger.debug('ENTER: player_move')
        game_id = str(int(action.game_id))

        try:
            game = cls.games[game_id]
            player_name = action.player_name
            game.process_move(player_name,action.move)
        except Exception as e:
            logger.debug('player_move_error: {}'.format(e))
            action.error = e
            action.notes = e

        end_hand = False

        if action.move == 'stay':
            end_hand = True
        elif not game.get_player(player_name).can_move():
            end_hand = True


        if end_hand:
            logger.debug('PLAYER NOT MOVING')
            game.dealer_move()
            game.evaluate_winners()
            game.payout_bets()

            logger.debug('ACTION-WINNERS: {}'.format(game.winners))
            if game.is_simple_winner(player_name):
                action.notes = 'Player won'
            else:
                action.notes = 'Dealer won'

            action.hands = game.get_cards(player_name)
            action.dealer_hand = game.get_dealer_cards()
            game.collect_cards()
        else:
            action.hands = game.get_cards(player_name)
            action.dealer_hand = game.get_dealer_cards()

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
        return cls.get_response(cls.games[action.game_id],action)
