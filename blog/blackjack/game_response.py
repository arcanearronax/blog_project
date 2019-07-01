import logging

logger = logging.getLogger('blog.blackjack.game_view')

# Used for game_api and game_master to communicate
class GameResponse():

    _fields = (
        'game_id',
        'player_name',
        'chip_count',
        'bet_amount',
        'player_hand',
        'player_score',
        'dealer_hand',
        'dealer_score',
        'result',
        'reason'
    )

    def __init__(self,*args,**kwargs):
        for k,v in kwargs.items():
            self.__setattr__(k,v)

    def __setattr__(self,k,v):
        if k in self.__class__._fields:
            super().__setattr__(k,v)
        else:
            raise AttributeError('Attribute not allowed.')

    def attrs(self):
        for attr, value in self.__dict__.items():
            yield attr,value
