from typing import Any
from django import forms
from .models import CustomerProfile
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserChangeForm,UserCreationForm


class UserForm(UserChangeForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        del self.fields["user_permissions"]
        del self.fields["is_superuser"]
        # del self.fields["groups"]
        del self.fields["is_staff"]
        del self.fields["is_active"]
        del self.fields["date_joined"]
        del self.fields["last_login"]


class NewUserForm(UserCreationForm):
    GROUPS = [(group.name, group.name)  for group in Group.objects.all()]
    group = forms.ChoiceField(choices=GROUPS, required=False)
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)



class CustomerProfileForm(forms.ModelForm):

    class Meta:
        model = CustomerProfile
        fields = "__all__"
        exclude = ["owner", "is_month_customer", "status"]
