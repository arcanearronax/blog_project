from .objects.card_deck import PlayingCardDeck
from .objects.player import BlackJackPlayer, BlackJackDealer
from .exceptions import GameException
from .game_action import GameAction
import logging

logger = logging.getLogger('blog.blackjack.game_view')

class BlackJackGame():
    _player_class = BlackJackPlayer

    def __init__(self,num_decks=1):
        self.dealer = BlackJackDealer()
        self.deck = PlayingCardDeck(num_decks,shuffle=True)
        self.players = dict()
        self.player_bets = {}
        self.player_done = {}
        self.winners = dict() #This has an appended value to indicate hand
        self.game_done = False

    #######################################
    ## Methods for getting object values ##
    #######################################

    def __repr__(self):
        return str(self.__dict__)

    def get_dealer(self):
        return self.dealer

    def get_deck(self):
        return self.deck

    def get_player(self,player_name):
        return self.players[player_name]

    # Return a list of player objects
    def get_players(self):
        return list(self.players.values())

    def get_bet(self,player_name):
        tmp = self.player_bets[player_name]
        logger.debug('GET BET: {} {}'.format(player_name,tmp))
        return tmp

    def get_bets(self):
        return self.player_bets

    def get_dealer_cards(self):
        return self.dealer.get_cards()

    ###############################
    ## Methods for adding values ##
    ###############################

    def add_player(self,player_name,chips):
        logger.debug('Enter: add_player {}'.format(player_name))
        self.players[player_name] = BlackJackPlayer(player_name,chips)

    def add_players(self,*args,**kwargs):
        for player_name,chips in kwargs.items():
            self.add_player(player_name,chips)

    def add_bet(self,player_name,bet):
        logger.debug('Enter: add_bet: {} {}'.format(player_name,bet))
        bet = int(bet)
        assert self.get_player(player_name).get_chips() >= bet, 'Insufficient chips for bet: {} - {}'.format(player_name,bet)
        self.player_bets[player_name] = bet

    def add_bets(self,**kwargs):
        for player_name,bet in kwargs.items():
            self.add_bet(player_name,bet)

    #################################
    ## Methods for clearing values ##
    #################################

    def collect_bet(self,player):
        player.take_chips(self.get_bet(player.get_name()))

    def collect_bets(self):
        for player in self.get_players():
            self.collect_bet(player)

    def collect_cards(self):
        for player in self.get_players():
            player.take_all_cards()
        self.dealer.take_all_cards()

    ################
    ## Game Logic ##
    ################

    # Determine moves the player can make
    # This needs some work
    def set_available_moves(self,player):
        logger.debug('Enter: set_available_moves')
        tup = ('stay',)
        if player.get_score() < 21 and player.get_card_count() < 5:
            tup = tup + ('hit',)
        elif player.get_card_count() == 2:
            tup = tup + ('double',)
            if player.get_card().face == player.get_card(card=1).face:
                tup = tup + ('split',)

        logger.debug('moves: {}'.format(tup))
        player.moves = tup

    def payout_bet(self,player_name):
        base_name = player_name[:-1]
        if self.winners[player_name]:
            self.get_player(base_name).give_chips(self.get_bet(base_name))
        else:
            self.get_player(base_name).take_chips(self.get_bet(base_name))

    def payout_bets(self):
        for player_name in self.winners:
            self.payout_bet(player_name)
        self.player_bets = dict()

    def is_simple_winner(self,player_name):
        # Just a quick and dirty way to figure out if someone won
        try:
            ret = self.winners[player_name + '0']
        except KeyError:
            return False
        else:
            return ret

    def evaluate_winner(self,hand):
        hand_score = hand.get_value()
        dealer_score = self.dealer.get_score()

        # Check for busts
        if hand_score > 21:
            return False
        elif dealer_score > 21:
            return True

        if hand_score > dealer_score:
            return True

        return False

    def evaluate_winners(self):
        for player in self.get_players():
            for ind,hand in enumerate(player.get_hands()):
                self.winners['{}{}'.format(player.get_name(),ind)] = self.evaluate_winner(hand)

    ##################
    ## Game Methods ##
    ##################

    # This is called when hands are dealt
    def deal_initial_hand(self):
        logger.debug('Enter: deal_initial_hand')
        for cnt in range(2):
            for player in self.get_players():
                player.give_card(self.deck.draw())
            if cnt == 1:
                self.get_dealer().give_card(self.deck.draw())
            else:
                self.get_dealer().give_card(self.deck.draw(hidden=True))

        logger.debug('DEALER: {}'.format(self.get_dealer().get_cards()))

        for player in self.get_players():
            for hand in player.get_hands():
                hand.set_available_moves()

    # This is called when the player hits
    def player_hit(self,player_name):
        logger.debug('HIT: {}'.format(player_name))
        self.get_player(player_name).give_card(self.deck.draw())
        if self.get_player(player_name).get_score() > 21:
            raise GameException('Hand score exceeds 21')

    # This is called when the player is done making moves
    def player_stay(self,player_name):
        self.dealer_move()

    # This is called when the player splits their hand
    def player_split(self,player_name):
        self.get_player(player_name).split_hand()
        self.add_card(player_name)
        self.add_card_split(player_name)

    # This is called when the player doubles
    def player_double(self,player_name):
        raise NotImplementedError()

    # This is called when players have finished or can't move
    def dealer_move(self):
        while self.get_dealer().get_score() < 16:
            self.get_dealer().give_card(self.deck.draw())
        self.dealer.hands[0][0].flip()
        self.round_done = True

    # This is called when the player makes a move
    def process_move(self,player_name,move):
        logger.debug('Enter: process_move - {} {}'.format(player_name, move))
        player = self.get_player(player_name)
        assert move in player._moves, 'Invalid Move Selection'

        eval('self.player_{}(player_name)'.format(move))

        # Have the players finished their moves?
        dealer_can_move = True
        for name,is_done in self.player_done.items():
            if not is_done:
                dealer_can_move = False
                break

        if dealer_can_move:
            self.dealer_move()







    # Just using this as a quick way to test stuff
    def get_cards(self,player_name):
        player = self.get_player(player_name)
        return player.get_cards()
