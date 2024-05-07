from django.forms import ModelForm
from .models import Feedback


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = "__all__"
        exclude = [
            "created_at",
            "is_published",
            "writer",
            "listing",
        ]
