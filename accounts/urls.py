from django.urls import path
from . import views



urlpatterns = [
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("edit-account/", views.edit_account, name="edit_account"),
    path("password-reset/", views.reset_password, name="reset_password"),
]
