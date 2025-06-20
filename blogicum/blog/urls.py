from django.urls import include, path

from . import views

app_name = "blog"

post_urls = [
    path("create/", views.PostCreateView.as_view(), name="create_post"),
    path("<int:post_id>/", views.PostDetailView.as_view(), name="post_detail"),
    path(
        "<int:post_id>/edit/", views.PostUpdateView.as_view(), name="edit_post"
    ),
    path(
        "<int:post_id>/delete/",
        views.PostDeleteView.as_view(),
        name="delete_post",
    ),
    path("<int:comment_id>/comment/", views.add_comment, name="add_comment"),
    path(
        "<int:post_id>/delete_comment/<int:comment_id>",
        views.CommentDeleteView.as_view(),
        name="delete_comment",
    ),
    path(
        "<int:post_id>/edit_comment/<int:comment_id>",
        views.CommentUpdateView.as_view(),
        name="edit_comment",
    ),
]

category_urls = [
    path(
        "<slug:category_slug>/",
        views.CategoryPostsView.as_view(),
        name="category_posts",
    ),
]

profile_urls = [
    path(
        "edit/",
        views.UserEditView.as_view(),
        name="edit_profile",
    ),
    path(
        "<str:username>/",
        views.UserProfileView.as_view(),
        name="profile",
    ),
]

urlpatterns = [
    path("posts/", include(post_urls)),
    path("category/", include(category_urls)),
    path("profile/", include(profile_urls)),
    path("", views.IndexView.as_view(), name="index"),
]
