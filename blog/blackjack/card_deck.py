from .card import PlayingCard
from .exceptions import CardDeckException
import random

class AbstractDeck():
    _card_class = None

    card_list = None

    def __init__(self,num_decks=1):
        tmp = []
        if (num_decks < 1):
            raise CardDeckException('Invalid Deck Number: {}'.format(num_decks))
        for _ in range(num_decks):
            for suit in self.__class__._card_class._suits:
                for face in self.__class__._card_class._faces:
                    tmp.append(self.__class__._card_class(suit,face))
        self.card_list = tmp

    def __str__(self):
        return str([str(x) for x in self.card_list])

    def shuffle(self):
        random.shuffle(self.card_list)

    def draw(self):
        return self.card_list.pop()

class PlayingCardDeck(AbstractDeck):
    _card_class = PlayingCard
