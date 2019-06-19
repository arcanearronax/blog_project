from .objects.card_deck import PlayingCardDeck
from .objects.player import BlackJackPlayer, BlackJackDealer
from .exceptions import GameException
from .game_action import GameAction
import logging

logger = logging.getLogger('blog.blackjack.game_view')

class BlackJackGame():
    _player_class = BlackJackPlayer

    def __init__(self,num_decks=1):
        self.players = {}
        self.bets = {}
        self.dealer = BlackJackDealer()
        self.deck = PlayingCardDeck(num_decks,shuffle=True)
        self.phase = 'init'
        self.player_done = False
        self.winners = dict()

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

    def get_dealer_cards(self):
        return self.dealer.get_cards()

    ###############################
    ## Methods for adding values ##
    ###############################

    def add_player(self,player_name,chips):
        player = BlackJackPlayer(player_name,chips)
        logger.debug('player_debug---{}'.format(player.__class__))
        self.players[player_name] = player

    def add_players(self,*args,**kwargs):
        for player_name,chips in kwargs.items():
            self.add_player()

    def add_bet(self,player_name,bet):
        try:
            bet = int(bet)
        except TypeError:
            raise GameException('Bet must be an int: {}'.format(bet.__class__.__name__))

        chip_count = self.get_player(player_name).get_chips()
        assert chip_count >= bet, 'Insufficient chips for bet: {} - {}'.format(player_name,bet)
        self.bets[player_name] = bet

    def add_bets(self,**kwargs):
        for player_name,bet in kwargs.items():
            self.add_bet(player_name,bet)

    #################################
    ## Methods for clearing values ##
    #################################

    def collect_bet(self,player):
        player.take_chips(self.bet[player.name])

    def collect_bets(self):
        for player in self.players:
            self.collect_bet(player)

    def collect_cards(self):
        for player in self.players:
            player.take_all_cards()

    ################
    ## Game Logic ##
    ################

    # Determine moves the player can make
    # This needs some work
    def set_available_moves(self,player_name):
        logger.debug('Enter: set_available_moves')
        player = self.players[player_name]
        tup = ('stay',)
        if player.get_score() < 21 and player.get_card_count() < 5:
            tup = tup + ('hit',)
        elif player.get_card_count() == 2:
            tup = tup + ('double',)
            if player.get_card().face == player.get_card(card=1).face:
                tup = tup + ('split',)

        logger.debug('moves: {}'.format(tup))
        player.moves = tup

    def deal_initial_hand(self):
        logger.debug('Enter: deal_initial_hand')
        for cnt in range(2):
            for player_name,player in self.players.items():
                logger.debug('PLAYER - {}'.format(player.__class__))
                player.give_card(self.deck.draw())
            if cnt == 1:
                self.dealer.give_card(self.deck.draw())
            else:
                self.dealer.give_card(self.deck.draw(hidden=True))

        logger.debug('DEALER: {}'.format(self.dealer.get_cards()))

        for player_name,player in self.players.items():
            self.set_available_moves(player_name)

    def player_hit(self,player_name):
        logger.debug('HIT: {}'.format(player_name))
        self.players[player_name].give_card(self.deck.draw())
        if self.players[player_name].get_score() > 21:
            raise GameException('Hand score exceeds 21')

    def player_stay(self,player_name):
        self.dealer_move()
        self.dealer.get_card().flip()

    def player_split(self,player_name):
        self.players[player_name].split_hand()
        self.add_card(player_name)
        self.add_card_split(player_name)

    def player_double(self,player_name):
        raise NotImplementedError()

    def dealer_move(self):
        if self.dealer.get_score() < 16:
            self.dealer.give_card(self.deck.draw())

    def evaluate_winner(self,hand=0):
        player_score = player.get_score(hand=hand)
        dealer_score = dealer.get_score()

        # Check for busts
        if player_score > 21:
            return False
        elif dealer_score > 21:
            return True

        if player_score > dealer_score:
            return True

        return False

    def evaluate_winners(self):
        for player_name,player in self.get_players().items():
            for ind,hand in enumerate(player.get_hands()):
                self.winners['{}{}'.format(player.name,ind)] = self.evaluate_winner(player.name,hand=ind)

    def payout_bet(self,player_name):
        base_name = player_name[:-1]
        if self.winners[player_name]:
            self.players[base_name].give_chips(self.get_bet(base_name))
        else:
            self.players[base_name].take_chips(self.get_bet(base_name))

    def payout_bets(self):
        for player_name in self.winners:
            self.payout_bet(player_name)
        self.bets = dict()

    def process_move(self,player_name,move):
        logger.debug('Enter: process_move - {} {}'.format(player_name, move))
        player = self.get_player(player_name)
        assert move in player._moves, 'Invalid Move Selection'

        eval('self.player_{}(player_name)'.format(move))

        if self.player_done:
            self.dealer_move()

    ###################
    ## Phase Routing ##
    ###################

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
        BlackJackGame._move_router[move](self,action)

    # Just using this as a quick way to test stuff
    def get_cards(self,player_name):
        player = self.players[player_name]
        return player.get_cards()
