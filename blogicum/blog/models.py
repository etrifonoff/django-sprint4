from core.models import PublishedAndCreatedAtModel
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Location(PublishedAndCreatedAtModel):
    name = models.CharField(max_length=256, verbose_name="Название места")

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return self.name


class Category(PublishedAndCreatedAtModel):
    title = models.CharField(max_length=256, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(
        unique=True,
        verbose_name="Идентификатор",
        help_text=(
            "Идентификатор страницы для URL; разрешены символы "
            "латиницы, цифры, дефис и подчёркивание."
        ),
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Post(PublishedAndCreatedAtModel):
    title = models.CharField(max_length=256, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    pub_date = models.DateTimeField(
        verbose_name="Дата и время публикации",
        help_text=(
            "Если установить дату и время в будущем — можно делать "
            "отложенные публикации."
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
        related_name="posts",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Местоположение",
        related_name="posts",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
        related_name="posts",
    )
    image = models.ImageField("Фото", upload_to="posts_images", blank=True)

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"

    def __str__(self):
        return self.title


class Comment(PublishedAndCreatedAtModel):
    text = models.TextField("Комментарий")
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="автор",
    )

    class Meta:
        ordering = ("created_at",)
        default_related_name = "comments"
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text
