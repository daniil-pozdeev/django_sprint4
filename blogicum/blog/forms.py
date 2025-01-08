from django import forms
from django.contrib.auth import get_user_model

from blog.models import Comment, Post

User = get_user_model()


class PostForm(forms.ModelForm):
    """Form for creating or updating a Post, excluding specific fields."""

    class Meta:
        model = Post
        exclude = ("author", )
        widgets = {
            "pub_date": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M"
            )
        }


class CommentForm(forms.ModelForm):
    """Form for submitting a comment with only text input."""

    class Meta:
        model = Comment
        fields = ("text", )


class UserUpdateForm(forms.ModelForm):
    """Form for updating user's basic profile information."""

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", )
