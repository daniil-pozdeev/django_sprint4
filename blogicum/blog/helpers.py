from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.utils import timezone

from blog.models import Post


def get_post_query_set(author=None, category=None):
    if author:
        kwargs = {"author": author}
    else:
        kwargs = {
            "is_published": True,
            "category__is_published": True,
            "pub_date__lte": timezone.now()
        }
    if category:
        kwargs = {
            "is_published": True,
            "category": category,
            "pub_date__lte": timezone.now()
        }
    return Post.objects.select_related(
        "category", "location", "author").filter(**kwargs).annotate(
            comment_count=Count("comments")).order_by("-pub_date")


def get_paginated_page(queryset, page_number, items_per_page):
    """
    Возвращает объект страницы для queryset.
    """
    paginator = Paginator(queryset, items_per_page)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не число, возвращаем первую страницу
        page = paginator.page(1)
    except EmptyPage:
        # Если page_number вне диапазона, возвращаем последнюю страницу
        page = paginator.page(paginator.num_pages)
    return page
