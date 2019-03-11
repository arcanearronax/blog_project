from django import forms
from django.forms import ModelForm, Textarea, Select
from .models import Post, Category, icon_choices

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        #choices = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
        fields = ('id','title','cat','text',)
        widgets = {
            'text': Textarea(attrs={'cols': 45, 'rows': 15}),
            'id': Textarea(attrs={'id':'post_id'})
        }

class CatForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('id','desc','hide',)

        choices = (
            ('hide', 'True',)
        )
        widgets = {
            'hide': forms.CheckboxInput(),
            'id': Textarea(attrs={'id':'cat_id'})
        }
