from django import forms
from django.forms import ModelForm, Textarea, Select
from .models import Post, Category, icon_choices

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        #choices = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
        fields = ('title','cat','text',)
        widgets = {
            'text': Textarea(attrs={'cols': 60, 'rows': 15})
        }

class CatForm(forms.ModelForm):
    class Meta:
        model = Category

        fields = ('desc','hide','icon',)

        choices = (
            ('hide', 'True',)
        )
        widgets = {
            'hide': forms.CheckboxInput(),
            'icon': Select(choices=icon_choices),
        }
