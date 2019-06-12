from .card_deck import PlayingCardDeck
from .player import BlackJackPlayer, BlackJackDealer
from .exceptions import GameException
from .game_action import GameAction
import logging

logger = logging.getLogger('blog.blackjack.game_api')

class BlackJackGame():

    def __init__(self,id,num_decks=1):
        self.id = id
        self.players = {}
        self.dealer = BlackJackDealer()
        self.deck = PlayingCardDeck(num_decks)
        self.pool = 0
        self.bets = {}

    ################################
    ## Methods for getting values ##
    ################################

    def get_players(self):
        return self.players

    def get_deck(self):
        return self.deck

    def get_bet(self,player):
        try:
            return self.bets['{}'.format(player)]
        except Exception as e:
            logger.error('get_bet_error: {}'.format(e))

    def get_bets(self):
        return self.bets

    def get_bets(self):
        return self.bets

    ################################
    ## Methods for getting values ##
    ################################

    def add_player(self,player):
        self.players[player.get_name()] = player

    def add_players(self,*args):
        for player in args:
            self.add_player(player)

    def add_deck(self,deck):
        self.shoe.extend(deck)

    def add_bet(self,player,bet):
        self.bets['{}'.format(player)] = bet

    def add_bets(self,**kwargs):
        for p,b in kwargs.items():
            self.add_bet(player,bet)



    ################
    ## Game Logic ##
    ################

    def deal_card_player(self,player,card):
        self.get_players()[player].give_card(card)

    def deal_initial_hand(self):
        for player in self.get_players():
            self.deal_card_player(player,self.deck.draw())

    def get_bets(self,**kwargs):
        assert len(kwargs) == len(self.get_players()), 'get_bets: Conflicting arg/players count'

        for player,bet in kwargs.items():
            self.players[player].take_chips(bet)
            self.bets[player] = bet

    def next_round(self):
        for name in self.get_players():
            print('({}: {})'.format(name,self.get_players()[name]))

            # The user interface will need to be laid out a bit more before this can be built out
            pass



    ###################
    ## Phase Routing ##
    ###################

    def create_player(self,action):
        logger.debug('Enter: create_player')

        self.add_player(BlackJackPlayer(action.player,action.chips))

    def place_bet(self,action):
        logger.debug('Enter: place_bet')

        self.add_bet(action.player,action.bet)

    _phase_router = {
        'create_player': create_player,
        'place_bet': place_bet,
    }



    #######################
    ## Action Processing ##
    #######################

    # Use this to comunicate with the API
    def process_action(self,action):
        logger.debug('ACTION: {}'.format(action.__dict__))

        return BlackJackGame._phase_router[action.phase](self,action)

    # This is a generic outline
    def main(self):

        # Initialize the gamephase = game.phase_id
        player = game.player
        bet_
        p1 = BlackJackPlayer('name1',50)
        p2 = BlackJackPlayer('name2',50)
        self.add_players(p1,p2)

        # Make bets
        self.get_bets(name1=10,name2=20)

        # Deal the hands
        self.deal_initial_hand()
        self.deal_initial_hand()
        print('Players: {}'.format(game.get_players()))
        for player in self.get_players():
            print('{}: count {}'.format(player, self.get_players()[player].get_chip_count()))

        # Check for next move
        self.next_round()
