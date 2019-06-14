import logging

logger = logging.getLogger(__name__)

# Used for game_api and game_master to communicate
class GameAction():

    _fields = ('game_id','phase','player','selection','chips','error','notes')
    _phase = ('create_player','place_bet','deal_hand')
    _actions = ('start','bet','hit','stay','split','double','stay')

    def __init__(self,**kwargs):
        for k,v in kwargs.items():
            self.__setattr__(k,v)

    def __setattr__(self,k,v):
        if k in self.__class__._fields:
            try:
                if v in eval('GameAction._{}'.format(k)):
                    super().__setattr__(k,v)
            except Exception as e:
                logger.debug('No _field for: {} - {}'.format(e,k))
                super().__setattr__(k,v)

    def process_action(self):
        if self.action == 'start':
            pass
