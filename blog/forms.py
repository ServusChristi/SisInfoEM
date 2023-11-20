from django import forms
from .models import Post

from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'body']
        widgets = {
            'author': forms.TextInput(attrs={"class": "form-control", "placeholder": "Seu Nome"}),
            'body': forms.Textarea(attrs={"class": "form-control", "placeholder": "Deixe um Comentário"})
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'categories']
