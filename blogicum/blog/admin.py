from django.contrib import admin

from blog.models import Category, Comment, Location, Post

admin.site.empty_value_display = "Не задано"


class PostTabilarInLine(admin.TabularInline):
    model = Post
    extra = 0


@admin.register(Post)
class PostAdimn(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "pub_date",
        "is_published",
        "created_at",
        "location",
        "category",
    )
    list_display_links = ("title",)
    list_editable = (
        "is_published",
    )

    search_fields = (
        "title",
    )
    list_filter = (
        "pub_date",
        "created_at",
        "location",
        "is_published",
        "author",
        "category",
    )
    readonly_fields = (
        "author",
        "created_at",
        "location",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "is_published",
        "created_at",
    )
    list_display_links = ("title",)
    list_editable = (
        "is_published",
    )

    search_fields = (
        "title",
    )
    list_filter = (
        "title",
        "created_at",
        "is_published",
    )
    readonly_fields = (
        "created_at",
    )
    inlines = (
        PostTabilarInLine,
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_published",
        "created_at",
    )
    list_display_links = ("name",)
    list_editable = (
        "is_published",
    )

    search_fields = (
        "name",
    )
    list_filter = (
        "created_at",
        "is_published",
    )
    readonly_fields = (
        "created_at",
    )
    inlines = (
        PostTabilarInLine,
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "post",
        "created_at",
        "author"
    )
    list_display_links = ("text",)
    search_fields = (
        "author__username",
    )
    list_filter = (
        "created_at",
    )
    readonly_fields = (
        "created_at",
    )
