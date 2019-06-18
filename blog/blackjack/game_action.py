from .exceptions import ActionException
import logging

logger = logging.getLogger('blog.blackjack.game_view')

# Used for game_api and game_master to communicate
class GameAction():

    _fields = ('game_id','phase','player_name','hands','move','chips','error','notes')
    _phase = ('create_player','start_round','initial_hand', 'player_move')
    _move = ('hit','stay','split','double')

    def __init__(self,**kwargs):
        for k,v in kwargs.items():
            self.__setattr__(k,v)

    def __str__(self):
        return str(self.__dict__)

    def __setattr__(self,k,v):
        if k in self.__class__._fields:
            try:
                if v in eval('GameAction._{}'.format(k)):
                    super().__setattr__(k,v)
                else:
                    raise ActionException('Assignment not allowed: {} - {}'.format(k,v))
            except Exception as e:
                super().__setattr__(k,v)

    def add_note(self,note):
        self.notes = note

    def add_error(self,error):
        self.error = error
