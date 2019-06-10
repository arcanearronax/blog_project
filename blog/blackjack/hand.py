from .card import PlayingCard
from .exceptions import HandException

class AbstractHand():
    _card_class = None
    _hand_limit = None

    _cards = []

    def add_card(self,card):
        assert self.get_card_count() < self._hand_limit, 'Cannot at card. Hand is at limit'
        self._cards.append(card)

    def get_cards(self):
        return self._cards

    def take_cards(self):
        self._cards = []


class PlayingCardHand(AbstractHand):
    _card_class = PlayingCard
    _hand_limit = 5

    def __init__(self):
        self._cards = []

    def __str__(self):
        cnt = 0
        ret = ''
        for card in self._cards:
            ret += '{}, '.format(card)
            cnt += 1
        return ret

    def __repr__(self):
        return str(self)

    def get_card_count(self):
        try:
            return len(self._cards)
        except Exception as e:
            return 0

    def get_total(self):
        value = 0
        for card in self._cards:
            value += card.get_value()
        return value
