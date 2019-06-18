from django import forms

class BlackJackForm(forms.Form):
    game_id = forms.CharField(label='game_id',max_length=10)
    player_name = forms.CharField(label='player_name',max_length=10)
    move = forms.CharField(label='move')
    phase = forms.CharField(label='phase')
    chips = forms.CharField(label='chips')
