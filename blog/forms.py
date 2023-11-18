from django import forms
from .models import Post


class CommentForm(forms.Form):
    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Seu Nome"}
        ),
    )
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Deixe um Comentário"}
        )
    )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'categories']
