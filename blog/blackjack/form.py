from django import forms

class BlackJackForm(forms.Form):
    game_id = forms.CharField(label='game_id',max_length=10)
    player = forms.CharField(label='player',max_length=10)
    selection = forms.CharField(label='selection')
    phase = forms.CharField(label='phase')
    chips = forms.CharField(label='chips')
