from .objects.card_deck import PlayingCardDeck
from .objects.player import BlackJackPlayer, BlackJackDealer
from .exceptions import GameException
from .game_action import GameAction
import logging

logger = logging.getLogger('blog.blackjack.game_api')

class BlackJackGame():
    _player_class = BlackJackPlayer

    def __init__(self,id,num_decks=1):
        self.players = {}
        self.bets = {}
        self.dealer = BlackJackDealer()
        self.deck = PlayingCardDeck(num_decks)

    ################################
    ## Methods for getting values ##
    ################################

    def __repr__(self):
        return str(self.__dict__)

    def get_player(self,player_name):
        try:
            return self.players[player_name]
        except KeyError:
            raise GameException('Player not found: {}'.format(player_name))

    def get_players(self):
        return self.players

    def get_deck(self):
        return self.deck

    def get_bet(self,player_name):
        try:
            return self.bets['{}'.format(player_name)]
        except KeyError:
            raise GameException('Bet not found: {}'.format(player_name))
        except Exception as e:
            logger.error('get_bet_error: {}'.format(e))

    def get_bets(self):
        return self.bets

    ###############################
    ## Methods for adding values ##
    ###############################

    def add_player(self,player,chips):
        player = BlackJackPlayer(player_name,chips)
        self.players[player_name] = ply

    def add_deck(self,deck):
        self.deck.extend(deck)

    def add_bet(self,player_name,bet):
        try:
            bet = int(bet)
        except TypeError:
            raise GameException('Bet must be an int')

        chip_count = self.players[player_name].get_chips()
        assert ply_count >= bet, 'Insufficient chips for bet: {}'.format(bet)
        self.bets[player_name] = bet

    def add_bets(self,**kwargs):
        for player_name,bet in kwargs.items():
            self.add_bet(player_name,bet)

    ################
    ## Game Logic ##
    ################

    def deal_initial_hand(self):
        for cnt in range(2):
            for player in self.players:
                player.give_card(self.deck.draw())
            self.dealer.add_card(hidden=True) if cnt == 2 else self.dealer.add_card(hidden=False)

    def player_hit(self,action):
        self.add_card(action.player)
        if self.players[action.player].hand.get_total() > 21:
            raise HandException('Hand score exceeds 21')

    def player_stay(self,action):
        return True

    def player_split(self,action):
        self.players[action.player].split_hand()
        self.add_card(action.player)
        self.add_card_split(action.player)


    def player_double(self,action):
        raise NotImplementedError()

    ###################
    ## Phase Routing ##
    ###################

    def create_player(self,action):
        logger.debug('Enter: create_player')
        self.add_player(action.player,action.chips)

    def place_bet(self,action):
        logger.debug('Enter: place_bet')
        self.add_bet(action.player,action.chips)

    def deal_cards(self,action):
        logger.debug('Enter: deal_cards')
        self.add_card(action.player)
        self.add_card(self.dealer,hidden=True)
        self.add_card(action.player)
        self.add_card(self.dealer)

    _move_router = {
        'hit': player_hit,
        'stay': player_stay,
        'split': player_split,
        'double': player_double,
    }

    # This may get called a few times, need to process logic based on hand
    def player_move(self,action):
        logger.debug('Enter: player_move')
        move = action.move
        try:
            if BlackJackGame._move_router[action.move](self,action):
                pass
            else:
                raise GameException('Move is not allowed')
        except HandAction as h:
            self.player_loss(action)
