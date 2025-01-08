from django.db.models import Count
from django.utils import timezone

from .models import Post


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
