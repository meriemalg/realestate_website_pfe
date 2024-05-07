from pprint import pprint
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import *
# Create your views here.
def edit_profile(request):
    profile_form = CustomerProfileForm(instance=request.user.customerprofile)

    if request.method == "POST":
        profile_form = CustomerProfileForm(
            request.POST, request.FILES, instance=request.user.customerprofile
        )
        if profile_form.is_valid():
            profile_form.save()
            pprint(profile_form.cleaned_data)
            messages.success(request, "changed submitted successfully")
            return redirect("dashboard")
        else:
            pprint("error: ", profile_form.errors) # type: ignore
            return redirect("edit_profile")

    context = {
        "profile_form": profile_form,
    }
    return render(request, "accounts/edit-profile.html", context)#Cette ligne rend le template HTML edit-profile.html avec les données spécifiées dans le dictionnaire context


def edit_account(request):

    user_form = UserForm(instance=request.user)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            pprint(user_form.cleaned_data)
            messages.success(request, "changed submitted successfully")
            return redirect("dashboard")
        else:
            pprint("error: ",user_form.errors) # type: ignore
            return redirect("edit_account")

    context = {
        "user_form": user_form,
    }
    return render(request, "accounts/edit-account.html", context)


from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User 

@login_required(login_url="login")
def reset_password(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password changed successfully")
            return redirect("dashboard")
    else:
        form = SetPasswordForm(user)
    return render(request, "accounts/password-reset.html", {"form": form})
