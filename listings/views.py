from pprint import pprint
from django.shortcuts import render
from listings.models import *
from accounts.models import *
from .models import Comment
from .forms import CommentForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def index(request):
    total_listings = (
        Listing.objects.all().filter(is_published=True).order_by("-add_date")
    )
    paginator = Paginator(total_listings, 6)  # Show
    page = request.GET.get("page", 1)
    listings = paginator.get_page(page)
    context = {"listings": listings}

    return render(request, "listings/listings.html", context)


def listing(request, listing_id):
    comments = Comment.objects.filter(
        listing_id=listing_id,
        is_published=True,
    )
    print("all the comments are:")
    pprint(comments)
    listing = Listing.objects.get(id=listing_id)
    comment_form = CommentForm()
    if request.method == "POST":
        print("request.POST is:")
        pprint(request.POST)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.listing = listing
            comment.user = request.user
            comment.save()
            messages.success(request, "comment saved successfully")
        else:
            messages.error(request, "comment not saved!")
    context = {
        "page_number": listing_id,
        "listing": listing,
        "comments": comments,
        "comment_form": comment_form,
    }
    return render(
        request, "listings/listing.html", context
    )  # Cette ligne de code renvoie une réponse HTTP qui rend un template HTML appelé 'listings/listing.html
