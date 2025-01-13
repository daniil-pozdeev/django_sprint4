from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.constants import PAGINATE_BY
from blog.forms import CommentForm, PostForm, UserUpdateForm
from blog.helpers import get_post_query_set
from blog.mixins import CommentUpdateDeleteMixin, PostUpdateDeleteMixin
from blog.models import Category, Comment, Post, User
from blog.helpers import get_paginated_page


def custom_post_list(request):
    queryset = Post.objects.filter(is_published=True).order_by("-pub_date")
    page_number = request.GET.get("page")
    page = get_paginated_page(queryset, page_number, items_per_page=10)

    return render(request, "blog/custom_list.html", {"page": page})


class PostListView(ListView):
    """List of published posts with comment count."""

    model = Post
    queryset = get_post_query_set()
    paginate_by = PAGINATE_BY
    template_name = "blog/index.html"


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a new post and set the author."""

    model = Post
    form_class = PostForm
    template_name = "blog/create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "blog:profile",
            kwargs={"username": self.request.user}
        )


class PostDetailView(DetailView):
    """Display detailed post info."""

    model = Post
    template_name = "blog/detail.html"
    pk_url_kwarg = "post_id"

    def get_object(self, queryset=None):
        post = super().get_object()

        if not post.is_published:
            if (
                not self.request.user.is_authenticated
                or post.author != self.request.user
            ):
                raise Http404("Публикация не найдена")

        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["comments"] = self.object.comments.select_related("author")
        return context


class PostUpdateView(LoginRequiredMixin, PostUpdateDeleteMixin, UpdateView):
    """Update a post."""

    model = Post
    pk_url_kwarg = "post_id"
    form_class = PostForm
    template_name = "blog/create.html"

    def get_success_url(self):
        return reverse("blog:post_detail", args=(self.object.pk,))


class PostDeleteView(LoginRequiredMixin, PostUpdateDeleteMixin, DeleteView):
    """Delete a post."""

    model = Post
    pk_url_kwarg = "post_id"
    template_name = "blog/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm()
        return context

    def get_success_url(self):
        return reverse("blog:profile", args=(self.request.user.username,))


class CategoryDetailView(ListView):
    """Display posts in a category."""

    model = Post
    template_name = "blog/category.html"
    paginate_by = PAGINATE_BY
    ordering = "-pub_date"

    def get_queryset(self):
        category = get_object_or_404(
            Category,
            slug=self.kwargs["category_slug"],
            is_published=True
        )
        return get_post_query_set(False, category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(
            slug=self.kwargs["category_slug"]
        )
        context["category"] = category
        return context


class UserListView(ListView):
    """Display user's posts."""

    model = Post
    template_name = "blog/profile.html"
    paginate_by = PAGINATE_BY
    ordering = "-pub_date"

    def get_queryset(self):
        user = get_object_or_404(
            User,
            username=self.kwargs["username"]
        )
        if self.request.user.username == self.kwargs["username"]:
            return get_post_query_set(user)
        return get_post_query_set().filter(author=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(User, username=self.kwargs["username"])
        context["profile"] = profile
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Update user profile."""

    model = User
    template_name = "blog/user.html"
    form_class = UserUpdateForm

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse("blog:profile", args=(self.request.user.username,))


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Create a comment."""

    model = Comment
    form_class = CommentForm
    template_name = "blog/comment.html"
    pk_url_kwarg = "post_id"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(
            Post,
            pk=self.kwargs["post_id"]
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post_detail", args=(self.object.post_id,))


class CommentUpdateView(LoginRequiredMixin,
                        CommentUpdateDeleteMixin, UpdateView):
    """Update a comment."""

    form_class = CommentForm


class CommentDeleteView(LoginRequiredMixin,
                        CommentUpdateDeleteMixin, DeleteView):
    """Delete a comment."""
