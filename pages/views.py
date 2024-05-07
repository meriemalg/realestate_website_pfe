from pprint import pprint
from django.shortcuts import render,redirect
from accounts.models import *
from announce.models import Announce
from contact.models import Contact, Order
from listings.models import *
from django.contrib import messages
from django.contrib import auth
from .models import Feedback
from .forms import FeedbackForm
from contact.views import send_email
# Create your views here.
def index(request):
    first_three=Listing.objects.order_by("-add_date")[:3]

    announcements = Announce.objects.filter(is_published=True).order_by("-add_date")
    context={
        "first_three":first_three,
        "announcements":announcements,
    }
    return render(request, 'pages/index.html',context)
def about(request):
    feedbacks = Feedback.objects.filter(
        is_published=True
    )
    agent_de_mois=RealtorProfile.objects.get(is_seller_of_month=True)
    agents=RealtorProfile.objects.all()
    feedback_form = FeedbackForm()
    if request.method == "POST":
        print("request.POST is:")
        pprint(request.POST)
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid() and not Feedback.objects.filter(writer=request.user).exists():
            feedback = feedback_form.save(commit=False)
            feedback.writer = request.user
            feedback.save()
            # send email to admin
            send_email(
                subject="New feedback",
        message=f"{request.user.username} with email {request.user.email if request.user.email else "[no email was set yet]"} has submitted a feedback",
                receiver_address=settings.EMAIL_HOST_USER
            )
            messages.success(request, "feedback saved successfully")
            return redirect("about")
        elif Feedback.objects.filter(writer=request.user).exists():
            messages.warning(
                request,
                "you have already submitted a feedback, you can't submit another one!"
            )
            return redirect("about")
        else:
            messages.error(request, "feedback not saved!")
    context = {
        "agent_de_mois": agent_de_mois,
        "agents": agents,
        "feedbacks": feedbacks,
        "feedback_form": feedback_form,
    }
    return render(request, 'pages/about.html',context)

from django.db.models import Q
def search(request):
    if request.method == "GET":
        return render(request, 'pages/search.html')
    if request.method == "POST":
        keywords = request.POST.get("keywords","")
        price = request.POST.get("price","")
        city = request.POST.get("city","")
        state = request.POST.get("state","")
        bedrooms = request.POST.get("bedrooms","")
        transaction_type = request.POST.get("transaction_type", "")
        print("transaction type selected is: ", transaction_type)
        # first level [published lists]
        search_listings = Listing.objects.filter(is_published=True)

        print("searched parmaeters are:")
        pprint(request.POST)
        q_objects = Q()
        if keywords:

            for field in ["title", "description", "realtor__owner__username"]:
                q_objects |= Q(**{f"{field}__icontains": keywords})
                new_search_listings = search_listings.filter(q_objects).distinct()
            print("# first level [lists that contain keywords]")
            print(new_search_listings)


        # third level [lists that contain city]
        if city:
            new_search_listings = search_listings.filter(
                city__icontains=city
            )

        # fourth level [lists that contain state]
        if state:
            new_search_listings = search_listings.filter(
                state__icontains=state
            )

        # fifth level [lists that contain bedrooms]
        if bedrooms:
            new_search_listings = search_listings.filter(
                bedrooms__lte=bedrooms
            )

        # sixth level [lists that contain price]
        if price:
            new_search_listings = search_listings.filter(
                price__lte=price
            )

        if transaction_type:
            new_search_listings = search_listings.filter(transaction_type=transaction_type)
            pprint(
                new_search_listings
            )

        print("final filter result is:")
        pprint(new_search_listings)
        context = {
            "listings":new_search_listings
        }
        return render(request, 'pages/search.html', context)

from accounts.forms import NewUserForm ,Group
def register(request):
    user_form = NewUserForm()

    if request.method == "POST":
        user_form = NewUserForm(request.POST)

        if user_form.is_valid():
            print("info validation processing...")
            new_user = User.objects.create_user(
                username=user_form.cleaned_data["username"],
                password=user_form.cleaned_data["password1"],
            )
            user_grp = Group.objects.get(name=user_form.cleaned_data["group"])
            new_user.groups.add(user_grp)
            new_user.save()
            print("account created successfully!")
            pprint(user_form.cleaned_data)
            messages.success(request, "account created successfully!")
            return redirect("dashboard")
        else:
            print("error: ", user_form.errors)
            messages.error(request,f"{user_form.errors}")  # type: ignore
            return redirect("register")

    context = {
        "user_form": user_form,
    }
    return render(request, "pages/register.html", context)


def logout(request):
    if request.method == "GET":
        auth.logout(request)
        messages.success(request,"logged out")
        return redirect("home")
    return render(request, 'pages/index.html')


def login(request):
    if request.method == "POST":
        given_username = request.POST.get("username", "")
        given_password = request.POST.get("password", "")
        pprint("user info:")
        pprint(request.POST)
        user_authenticated = User.objects.filter(username=given_username).first()
        # print("user password is: ", user_authenticated.password) # type: ignore

        if user_authenticated:
            user_authenticated = auth.authenticate(request, username=given_username, password=given_password)
            if user_authenticated:
                auth.login(request, user_authenticated)
                messages.success(request, "logged in successfully")
                return redirect("home")
            else:
                messages.error(request, "password or username are not correct!")
                return redirect("login")
        else:
            messages.error(
                request, f"no such a user with the name {given_username} in the database!"
            )
    return render(request, "pages/login.html")


from django.contrib.auth.decorators import login_required
@login_required(login_url="login")
def dashboard(request):
    customer=CustomerProfile.objects.filter(owner=request.user).exists()
    if not customer:
        messages.error(request, "Your account needs to be validated by admin first!")
        return redirect("home")
    customer = CustomerProfile.objects.get(owner=request.user)
    user_contacts = Contact.objects.order_by("-consultation_date").filter(
        customer=customer
    )
    user_orders = Order.objects.order_by("-purchase_date").filter(
        customer=request.user
    )
    pprint(user_contacts)
    context = {
        "contacts": user_contacts,
        "orders": user_orders,
    }
    return render(request, "pages/dashboard.html", context)


def delete_order(request, order_id):

    Order.objects.get(pk=order_id).delete()
    messages.warning(request, f"Order has been deleted!")

    return redirect("dashboard")
