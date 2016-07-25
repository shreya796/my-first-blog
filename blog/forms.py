from django import forms

from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post #will follow the Post Model
        fields = ('title', 'text',)