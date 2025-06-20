from blog.models import Post
from django.db.models import Count
from django.utils import timezone


def filter_posts(
    manager=Post.objects, apply_filters=True, add_annotations=False
):
    queryset = manager.select_related("author", "location", "category")

    if apply_filters:
        queryset = queryset.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        )

    if add_annotations:
        queryset = queryset.annotate(comment_count=Count("comments")).order_by(
            "-pub_date"
        )

    return queryset
    return queryset
    return queryset
    return queryset
