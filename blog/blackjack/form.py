from django import forms

class BlackJackForm(forms.Form):
    game_id = forms.CharField(label='game_id',max_length=10)
    player = forms.CharField(label='player',max_length=10)
    bet_amount = forms.CharField(widget=forms.TextInput(attrs={'type':'number'}))
    selection = forms.CharField(label='selection')
