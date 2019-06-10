from .exceptions import CardException

class AbstractCard():

    _suits = None
    _faces = None

    def __init__(self,suit,face):
        self.suit = suit
        self.face = face
        self.hidden = True

    def __str__(self):
        if self.hidden:
            return 'hidden_card'
        return '{} of {}'.format(self.get_face(),self.get_suit())


    def __repr__(self):
        return str(self)

    def __setattr__(self,attr,value):
        if attr == 'suit':
            if value not in self.__class__._suits:
                raise CardException('Invalid suit: {}'.format(value))
        elif attr == 'face':
            if value not in self.__class__._faces:
                raise CardException('Invalid face: {}'.format(value))
        super().__setattr__(attr,value)

    def __add__(self,other):
        raise NotImplementedError('Subclass must implement this method')

    def get_suit(self):
        return self.suit

    def get_face(self):
        return self.face

    def get_value(self):
        raise NotImplementedError('Subclass must implement this method')

    def reveal(self):
        self.hidden = False

class PlayingCard(AbstractCard):
    _suits = ('Clubs','Diamonds','Hearts','Spades')
    _faces_special = ('Jack','Queen','King','Ace')
    _faces = (2,3,4,5,6,7,8,9,10) + _faces_special

    def get_value(self):
        face = self.get_face()
        value = None
        if face in self.__class__._faces_special:
            if face == 'Ace':
                value = 11
            else:
                value = 10
        else:
            value = face
        return value

    def __add__(self,other):
        assert other.__class__.__name__ == 'PlayingCard', 'Unsupported class: {}'.format(other.__class__)

        sum = self.get_value() + other.get_value()
        if sum == 22:
            sum -= 10
        return sum
