from django.contrib import admin

from .models import Category, Comment, Location, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "pub_date", "author")
    list_editable = ("category",)
    search_fields = ("title", "text")
    list_filter = ("pub_date", "category")
    ordering = ("-pub_date",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_published")
    search_fields = ("title",)
    list_filter = ("is_published",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published")
    search_fields = ("title",)
    list_filter = ("is_published",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "text", "author", "created_at")
    search_fields = ("text",)
    list_filter = ("created_at",)
