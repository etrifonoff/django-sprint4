from django import forms
from django.core.mail import send_mail

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ("author",)
        widgets = {
            "pub_date": forms.DateTimeInput(
                format="%Y-%m-%d %H:%M:%S", attrs={"type": "datetime-local"}
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)

    def clean(self):
        super().clean()
        text = self.cleaned_data["text"]
        send_mail(
            subject="Another Beatles member",
            message=f"{text} пытался написать коммент!",
            from_email="birthday_form@acme.not",
            recipient_list=["admin@acme.not"],
            fail_silently=True,
        )
