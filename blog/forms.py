from django import forms
from .models import Post, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        #choices = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
        fields = ('title','cat','text',)
