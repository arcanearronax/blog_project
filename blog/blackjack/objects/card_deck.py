from .card import PlayingCard
from ..exceptions import DeckException
import random
import logging

logger = logging.getLogger('blog.blackjack.game_api')

class AbstractDeck():
    _card_class = None

    def __init__(self,num_decks=1,hidden=True,shuffle=False):
        tmp = []
        if (num_decks < 1):
            raise CardDeckException('Invalid Deck Number: {}'.format(num_decks))
        for _ in range(num_decks):
            for suit in self.__class__._card_class._suits:
                for face in self.__class__._card_class._faces:
                    tmp.append(self.__class__._card_class(suit,face))

        self.card_list = tmp
        if shuffle:
            self.shuffle()

    def __str__(self):
        return str([str(x) for x in self.card_list])

    def __repr__(self):
        return str(list(x for x in self.card_list))

    def shuffle(self):
        random.shuffle(self.card_list)

    def draw(self,hidden=False):
        try:
            card = self.card_list.pop()
        except IndexError as i:
            raise DeckException('No cards remaining')

        if hidden:
            card.flip()
        return card

class PlayingCardDeck(AbstractDeck):
    _card_class = PlayingCard
