from django.shortcuts import redirect
from django.urls import reverse

from .forms import CommentForm
from .models import Comment


class PostUpdateDeleteMixin:
    """Mixin to check authorship when updating and deleting a post."""

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect("blog:post_detail", self.get_object().pk)
        return super().dispatch(request, *args, **kwargs)


class CommentUpdateDeleteMixin:
    """Mixin to check authorship when updating and deleting a comment."""

    model = Comment
    form_class = CommentForm
    template_name = "blog/comment.html"
    pk_url_kwarg = "comment_id"

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect("blog:post_detail", self.get_object().post_id)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        post_id = self.get_object().post_id
        return reverse("blog:post_detail", args=(post_id,))
