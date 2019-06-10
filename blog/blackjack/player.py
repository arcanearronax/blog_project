from .hand import PlayingCardHand
from .exceptions import PlayerException

class AbstractPlayer():
    hand = None

    def __init__(self,name):
        if name.__class__.__name__ != 'str':
            raise PlayerException('Player name must be a string')
        self.name = name

    def __str__(self):
        print('HAND: {}'.format(self.get_hand().__class__))
        return '{}: {}'.format(self.name, self.get_hand().get_cards())

    def __repr__(self):
        return str(self)

    def get_name(self):
        return self.name

    def get_hand(self):
        return self.hand

    def give_card(self,card):
        self.hand.add_card(card)

    def take_cards(self):
        self.hand.take_cards()

class BlackJackPlayer(AbstractPlayer):
    _moves_allowed = ('hit','split','double','stay')

    def __init__(self,name,chips):
        self.chips = chips
        self.hand = PlayingCardHand()
        self.moves_allowed = BlackJackPlayer._moves_allowed
        self.bust = False
        super().__init__(name)

    def get_chip_count(self):
        return self.chips

    def take_chips(self,chips):
        chip_count = self.get_chip_count()
        if chips > chip_count:
            raise PlayerException('Cannot take chips: {} {}'.format(chips, chip_count))
        else:
            self.chips -= chips

    def get_moves_allowed(self):
        return self.moves_allowed

    def give_card(self,card):
        super().give_card(card)
        if self.get_hand().get_total() > 21:
            self.bust = True

    def to_do():
        raise NotImplementedError()

class BlackJackDealer(BlackJackPlayer):

    def __init__(self,chips=1000000):
        super().__init__('Dealer',chips)
