import logging

logger = logging.getLogger(__name__)

class GameAction():

    _fields = ('game_id','phase','player','selection','bet_amount',)
    _actions = ('start','bet','hit','stay','split','double','stay')

    def __init__(self,**kwargs):
        for k,v in kwargs.items():
            self.__setattr__(k,v)

    def __setattr__(self,k,v):
        if k in self.__class__._fields:
            super().__setattr__(k,v)

    def process_action(self):
        if self.action == 'start':
            pass
