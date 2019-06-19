from .hand import PlayingCardHand
from ..exceptions import PlayerException,HandException
import logging

logger = logging.getLogger('blog.blackjack.game_view')

class AbstractPlayer():
    _hand_class = None

    def __init__(self,name):
        name_cls = name.__class__.__name__
        if name_cls != 'str':
            raise PlayerException('Player name must be a string: {}'.format(name_cls))
        self.name = name

    def __str__(self):
        return '{}'.format(self.name)

    def __repr__(self):
        return str(self.__dict__)

class BlackJackPlayer(AbstractPlayer):
    _hand_limit = 2
    _hand_class = PlayingCardHand
    _moves = ('stay','hit','double','split')

    def __init__(self,name,chips):
        chips = self.__class__.validate_chips(chips)
        self.chips = chips
        self.hands = [self.__class__._hand_class()]
        self.moves = ()
        super().__init__(name)

    def __str__(self):
        hands = []
        for hand in self.hands:
            hands.append(str(hand))
        return '({},{},{})'.format(self.name,self.chips,hands)

    def disable_move(self,move):
        self.moves = tuple(m for m in self.moves if m != move)

    def enable_move(self,move):
        self.moves += (move,)

    ##################
    ## Chip Methods ##
    ##################

    def get_chips(self):
        return int(self.chips)

    def validate_chips(chips):
        try:
            return int(chips)
        except TypeError:
            raise PlayerException('Chips must be cast as int: {}'.format(chips.__class__.__name__))
        except ValueError:
            raise PlayerException('Chips must be cast as int: {}'.format(chips))

    def give_chips(self,chips):
        chips = self.__class__.validate_chips(chips)
        self.chips += chips

    def take_chips(self,chips):
        chip_count = self.get_chips()
        chips = self.__class__.validate_chips(chips)
        print('CHIP CLASS: {}'.format(chips.__class__))
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
        try:
            return self.hands[hand].get_cards()
        except IndexError:
            raise PlayerException('Hand does not exist: {}'.format(hand))

    def give_card(self,card,hand=0):
        try:
            self.hands[hand].give_card(card)
        except IndexError:
            raise PlayerException('Hand does not exist: {}'.format(hand))
        except AssertionError:
            raise PlayerException('Hand is at limit: {}'.format(self.hands[hand].get_card_count()))

    def give_cards(self,*args,hand=0,**kwargs):
        for card in args:
            self.give_card(card,hand=hand)

    def take_card(self,hand=0,card=0):
        try:
            return self.hands[hand].take_card(card)
        except HandException as h:
            raise PlayerException('Card index is invalid: {}'.format(hand))
        except IndexError:
            raise PlayerException('Hand index does not exist: {}'.format(hand))

    def take_cards(self,hand=-1):
        try:
            return self.hands[hand].take_cards()
        except IndexError:
            raise PlayerException('Hand index does not exist: {}'.format(hand))

    def take_all_cards(self):
        cards = []
        for hand in self.hands:
            cards += hand
        self.hands = [self.__class__._hand_class()]
        return cards

    ##################
    ## Hand Methods ##
    ##################

    def get_hand(self,hand=0):
        try:
            return self.hands[hand]
        except IndexError:
            raise PlayerException('Hand does not exist: {}'.format(hand))

    def get_hands(self):
        return self.hands

    ###################
    ## Logic Methods ##
    ###################

    def get_score(self,hand=0):
        score = self.hands[hand].get_value()
        logger.debug('GetScore - {}'.format(score))
        return score

    def get_card_count(self,hand=0):
        cnt = self.hands[hand].get_card_count()
        logger.debug('GetCardCount - {}'.format(cnt))
        return cnt

    def can_move(self):
        ret = False
        if self.get_card_count() < self.__class__._hand_limit:
            if self.get_score() < 21:
                ret = True

        return ret

class BlackJackDealer(BlackJackPlayer):

    def __init__(self,chips=1000000):
        super().__init__('Dealer',chips)
