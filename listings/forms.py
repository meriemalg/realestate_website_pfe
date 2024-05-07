from django.forms import ModelForm
from .models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        exclude = [
            "post",
            "created_at",
            "is_published",
            "user",
            "listing",
        ]
        labels = {
            "content": "Your Comment",
        }
