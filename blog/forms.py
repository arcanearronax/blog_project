from django import forms
from django.forms import ModelForm, Textarea
from .models import Post, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        #choices = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
        fields = ('title','cat','text',)
        widgets = {
            'text': Textarea(attrs={'cols': 60, 'rows': 15})
        }
