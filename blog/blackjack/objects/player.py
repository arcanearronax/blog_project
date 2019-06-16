from .hand import PlayingCardHand
from ..exceptions import PlayerException

class AbstractPlayer():
    _hand_class = None

    def __init__(self,name,*args,**kwargs):
        name_cls = name.__class__.__name__
        if name_cls != 'str':
            raise PlayerException('Player name must be a string: {}'.format(name_cls))
        self.name = name

    def __str__(self):
        return '{}'.format(self.name)

    def __repr__(self):
        return str(self.__dict__)

    def get_name(self):
        return self.name

    def get_hand(self):
        return self.hand

    def give_card(self,card):
        self.hand.add_card(card)

    def take_cards(self):
        self.hand.take_cards()

    def do_action(self,action):
        print('DOING: {}'.format(action))

class BlackJackPlayer(AbstractPlayer):
    _hands_limit = 2
    _hand_class = PlayingCardHand

    def __init__(self,name,chips):
        self.chips = chips
        self.hands = [self.__class__._hand_class()]
        super().__init__(name)

    def __str__(self):
        return '({},{},{})'.format(self.name,self.chips,self.hands)

    ##################
    ## Chip Methods ##
    ##################

    def get_chips(self):
        return int(self.chips)

    def give_chips(self,chips):
        chips_cls = chips.__class__.__name__
        assert chips_cls == 'int', 'Chips must be int: {}'.format(chips_cls)
        self.chips += chips

    def take_chips(self,chips):
        chip_count = self.get_chips()
        chips_cls = chips.__class__.__name__
        assert chips_cls == 'int', 'Chips must be int: {}'.format(chips_cls)
        if chips > chip_count:
            raise PlayerException('Chip request exceed amount: {}'.format(chip_count))
        else:
            self.chips -= chips

    ##################
    ## Card Methods ##
    ##################

    def get_card(self,hand=0,card=0):
        try:
            return self.hands[hand].get_card(card)
        except HandException as h:
            raise PlayerException('Card does not exist in hand: {}-{}'.format(hand,card))

    def get_cards(self,hand=0):
        return self.hands[hand].get_cards()

    def give_card(self,card,hand=0):
        try:
            self.hands[hand].give_card(card)
        except AssertionError as a:
            raise PlayerException('Hand is at limit: {}'.format(self.hands[hand].get_card_count()))

    def give_cards(self,*args,hand=0,**kwargs):
        for card in args:
            self.give_card(card,hand=hand)

    def take_card(self,hand=0,card=0):
        try:
            return self.hands[hand].take_card(card)
        except HandException as h:
            raise PlayerException(h)

    def take_cards(self,hand=-1):
        if hand == -1:
            cards = []
            for hand in self.hands:
                cards += hands
            self.hands = [self.__class__._hand_class()]
            return cards
        return self.hands[hand].take_cards()

    ##################
    ## Hand Methods ##
    ##################


class BlackJackDealer(BlackJackPlayer):

    def __init__(self,chips=1000000):
        super().__init__('Dealer',chips)
