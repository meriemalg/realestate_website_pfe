from pprint import pprint
from django.shortcuts import redirect, render
from accounts import*
from .models import *
from listings.models import *
from django.contrib   import messages
from django.core.mail import send_mail
# Create your views here.

import smtplib


def send_email(subject, message, receiver_address="yawapen977@acentni.com"):
    # Your email address and password
    sender_address = "meriemmeriem19alg@gmail.com"
    sender_password = "kdza nxxy ywus oyyc"

    # Set up the subject and body of the email
    header = f"\r\nSubject: {subject}"
    body = f"\r\n{message}"

    # Combine the headers and the body
    combined = header + body

    # Send the email!
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender_address, sender_password)
    server.sendmail(sender_address, receiver_address, combined)
    print("Email sent!")


def contact(request):
    if request.method=="POST":
        listingid=request.POST.get('listing_id',"")

        name=request.POST.get('name',"")
        title=request.POST.get('title',"")
        email=request.POST.get('email',"")
        message=request.POST.get('message',"")
        if listingid and name and title and message:
            customer=CustomerProfile.objects.get(owner=request.user)
            listing=Listing.objects.get(id=listingid)
            contact=Contact(
                real_state=listing,
                customer=customer,
                title=title,
                content=message,
            )
            print("the new contact",contact)
            contact.save()

            try:
                send_email(
                    f"inquiry about {title} by {customer.owner.username} sent by {request.user.email}",
                    f"{message}",
                    email # type: ignore
                ) # type: ignore
                # send_mail(
                #     f"inquiry about {title} by {customer.owner.username}",
                #     f"{message}",
                #     request.user.email,
                #     [listing.realtor.owner.email], # type: ignore
                #     fail_silently=False
                # ) # type: ignore
            except Exception as e:#erreur lors de l'envoie d'un email
                print("ERROR: ",e)
            pprint(contact)
            messages.success(request,"contact saved successfuly")
            return redirect("dashboard")
        else:
            messages.error(request,"one of the files is not given")
            return redirect("listing", listingid)


def order(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        transaction_type = request.POST["transaction_type"]
        print("transaction_type: ", transaction_type)
        listing = Listing.objects.get(id=listing_id)
        #  Check if user has made inquiry already
        if request.user.is_authenticated:

            has_ordered = Order.objects.all().filter(
                listing_id=listing_id, customer=request.user
            )
            if has_ordered:
                messages.error(
                    request, "You have already made an inquiry for this listing"
                )
                return redirect("/listings/" + listing_id)

            else:
                new_order = Order(
                    listing=listing,
                    customer=request.user,
                    email=request.user.email,
                    transaction_type=transaction_type,
                )
                new_order.save()
                messages.success(request, "Order saved successfully!")
                return redirect("dashboard")

        messages.success(
            request,
            "Your request has been submitted, a realtor will get back to you soon",
        )
        return redirect("/listings/" + listing_id)
