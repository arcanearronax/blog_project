from django import forms
from django.forms import ModelForm, Textarea
from .models import Post, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        #choices = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
        fields = ('post_id','title','cat','text',)
        widgets = {
            'text': Textarea(attrs={'cols': 45, 'rows': 15}),
            'post_id': Textarea(attrs={'style':'display:none'}),
        }

class CatForm(forms.ModelForm):
    class Meta:
        model = Category

        fields = ('cat_id','desc','hide',)

        choices = (
            ('hide', 'True')
        )
        widgets = {
            'hide': forms.CheckboxInput(),
            'cat_id': Textarea(attrs={'style':'display:none', 'id':'cat_id'})
        }

class LoginForm(forms.Form):
    username= forms.CharField(max_length= 25,label="Enter username")
    password= forms.CharField(max_length= 30, label='Password', widget=forms.PasswordInput)
