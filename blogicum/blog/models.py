from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import Truncator

from core.models import PublishedAndCreatedModel
from blog.constants import LEN_COMMENT, LEN_TEXT_FILD

User = get_user_model()


class Category(PublishedAndCreatedModel):
    """Defines a post category, inheriting publication and creation fields."""

    title = models.CharField(
        max_length=LEN_TEXT_FILD,
        verbose_name="Заголовок"
    )
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(
        unique=True,
        help_text=("Идентификатор страницы для URL; разрешены "
                   "символы латиницы, цифры, дефис и подчёркивание."),
        verbose_name="Идентификатор",
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return (Truncator(self.title).chars(LEN_COMMENT))


class Location(PublishedAndCreatedModel):
    """Represents a location for associative posts."""

    name = models.CharField(
        max_length=LEN_TEXT_FILD,
        verbose_name="Название места"
    )

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self) -> str:
        return (Truncator(self.name).chars(LEN_COMMENT))


class Post(PublishedAndCreatedModel):
    """Blog post with metadata: location, category, author."""

    title = models.CharField(
        max_length=LEN_TEXT_FILD,
        verbose_name="Заголовок"
    )
    text = models.TextField(verbose_name="Текст")
    pub_date = models.DateTimeField(
        help_text=("Если установить дату и время "
                   "в будущем — можно делать отложенные публикации."),
        verbose_name="Дата и время публикации",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Местоположение",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
    )
    image = models.ImageField(
        blank=True,
        upload_to="posts_images",
        verbose_name="Фото",
    )

    class Meta:
        default_related_name = "posts"
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"

    def __str__(self) -> str:
        return (Truncator(self.title).chars(LEN_COMMENT))


class Comment(models.Model):
    """Represents a comment made by a user on a specific post."""

    text = models.TextField(verbose_name="Текст комментария")
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        default_related_name = "comments"
        ordering = ("created_at",)
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self) -> str:
        return self.post
