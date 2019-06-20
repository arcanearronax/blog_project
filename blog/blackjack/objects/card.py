from ..exceptions import CardException
import logging

logger = logging.getLogger('blog.blackjack.game_view')

class AbstractCard():

    _restricted_fields = None
    _suits = None
    _faces = None

    # It's up to the subclass to validate attributes
    def __init__(self,*args,**kwargs):
        for k,v in kwargs.items():
            self.__setattr__(k,v)

    def __str__(self):
        raise NotImplementedError('Subclass must implement this method')

    def __repr__(self):
        return str(self.__dict__)

    # This will handle validating restricted attributes
    def __setattr__(self,attr,value):
        if attr in self.__class__._restricted_fields:
            if value not in eval('self.__class__._{}s'.format(attr)):
                raise CardException('Invalid {}: {}'.format(attr,value))
        super().__setattr__(attr,value)

    def flip(self):
        self.hidden = not self.hidden

class PlayingCard(AbstractCard):
    _restricted_fields = ('suit','face')
    _suits = ('Clubs','Diamonds','Hearts','Spades')
    _face_values = {
        'Ace': 11,
        'King': 10,
        'Queen': 10,
        'Jack': 10,
        '10': 10,
        '9': 9,
        '8': 8,
        '7': 7,
        '6': 6,
        '5': 5,
        '4': 4,
        '3': 3,
        '2': 2,
    }
    _faces = list(_face_values)

    def __init__(self,suit,face,hidden=False):
        super().__init__(suit=suit,face=face,hidden=hidden)

    def __str__(self):
        if self.hidden:
            return 'hidden_card'
        return '{} of {}'.format(self.face,self.suit)

    def get_value(self):
        return PlayingCard._face_values[self.face]

    def __add__(self,other):
        assert other.__class__ == self.__class__, 'Unsupported class: {}'.format(other.__class__)
        return self.get_value() + other.get_value()
