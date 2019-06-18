from .card import PlayingCard
from ..exceptions import DeckException
import random
import logging

logger = logging.getLogger('blog.blackjack.game_view')

class AbstractDeck(list):
    _card_class = None

    def __init__(self,num_decks=1,hidden=True,shuffle=False):
        tmp = []
        if (num_decks < 1):
            raise CardDeckException('Invalid Deck Number: {}'.format(num_decks))
        for _ in range(num_decks):
            for suit in self.__class__._card_class._suits:
                for face in self.__class__._card_class._faces:
                    self.append(self.__class__._card_class(suit,face))

        if shuffle:
            self.shuffle()

    def __str__(self):
        return str([str(x) for x in self])

    def __repr__(self):
        return str(list(x for x in self))

    def shuffle(self):
        random.shuffle(self)

    def draw(self,hidden=False):
        try:
            card = self.pop(0)
        except IndexError:
            raise DeckException('No cards remaining')

        if hidden:
            card.flip()
        return card

class PlayingCardDeck(AbstractDeck):
    _card_class = PlayingCard
