from django.db import models
from accounts.models import *
from listings.models import *
from datetime import datetime

class Contact(models.Model):
    customer=models.ForeignKey(CustomerProfile,on_delete=models.CASCADE)
    real_state=models.ForeignKey(Listing, on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    content=models.TextField()
    consultation_date=models.DateTimeField(auto_now_add=True)
    is_reviewed=models.BooleanField(default=False)
    reponse_status=models.BooleanField(default=False)
    response_content = models.TextField(default="")
    last_answer = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.customer} contacted {self.real_state}'

class Order(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    email = models.CharField(max_length=100)

    class Status(models.TextChoices):
        IN_INSTALLEMENTS = "par versement"
        CONTRACT = "par contrat de location"
        CASH = "payee"
    transaction_type = models.CharField(
        max_length=50, choices=[("allouer", "allouer"), ("vendre","vendre")]
    )
    discount = models.DecimalField(decimal_places=2, max_digits=5, default=0) # type: ignore
    status = models.CharField(max_length=23, choices=Status.choices, default=Status.CASH)

    purchase_date = models.DateTimeField(auto_now=True)
    
    rent_or_installement_payement_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.listing.title} purchased by {self.customer}' # type: ignore
