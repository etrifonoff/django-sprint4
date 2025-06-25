from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.constants import POSTS_LIMIT
from blog.filters import filter_posts
from blog.forms import CommentForm, PostForm
from blog.mixins import CommentMixin, OnlyAuthorMixin
from blog.models import Category, Post


@login_required
def add_comment(request, comment_id):
    post = get_object_or_404(Post, pk=comment_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect("blog:post_detail", post_id=comment_id)


class IndexView(ListView):
    model = Post
    template_name = "blog/index.html"
    paginate_by = POSTS_LIMIT
    ordering = "-pub_date"

    def get_queryset(self):
        return filter_posts(add_annotations=True)


class CategoryPostsView(ListView):
    model = Post
    template_name = "blog/category.html"
    paginate_by = POSTS_LIMIT

    def get_category(self):
        return get_object_or_404(
            Category, slug=self.kwargs["category_slug"], is_published=True
        )

    def get_queryset(self):
        selected_category = self.get_category()
        return filter_posts(
            manager=selected_category.posts,
        ).order_by("-pub_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_category()
        context["category"] = category
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "blog:profile", kwargs={"username": self.request.user.username}
        )


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    post_key = "post_id"
    pk_url_kwarg = "post_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["comments"] = self.object.comments.select_related("author")
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user_posts = Post.objects.filter(author=self.request.user)
            published_posts = filter_posts()
            return user_posts | published_posts
        return filter_posts()


class PostUpdateView(LoginRequiredMixin, OnlyAuthorMixin, UpdateView):
    template_name = "blog/create.html"
    model = Post
    form_class = PostForm
    pk_url_kwarg = "post_id"

    def handle_no_permission(self):
        return redirect(
            "blog:post_detail", post_id=self.kwargs[self.pk_url_kwarg]
        )

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"post_id": self.object.id})


class PostDeleteView(LoginRequiredMixin, OnlyAuthorMixin, DeleteView):
    template_name = "blog/create.html"
    model = Post
    pk_url_kwarg = "post_id"

    def get_success_url(self):
        return reverse(
            "blog:profile", kwargs={"username": self.request.user.username}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm(instance=self.object)
        return context


class CommentUpdateView(
    LoginRequiredMixin, CommentMixin, OnlyAuthorMixin, UpdateView
):
    form_class = CommentForm


class CommentDeleteView(LoginRequiredMixin, CommentMixin, DeleteView):
    pass


class UserProfileView(ListView):
    model = Post
    template_name = "blog/profile.html"
    paginate_by = POSTS_LIMIT

    def get_user(self):
        return get_object_or_404(User, username=self.kwargs["username"])

    def get_queryset(self):
        selected_user = self.get_user()
        queryset = filter_posts(
            manager=selected_user.posts,
            apply_filters=selected_user != self.request.user,
            add_annotations=True,
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_user()
        return context


class UserEditView(LoginRequiredMixin, UpdateView):
    template_name = "blog/user.html"
    model = User
    fields = ["first_name", "last_name", "email"]

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            "blog:profile", kwargs={"username": self.object.username}
        )
