from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class CustomerProfile(models.Model):
    profile_image = models.ImageField(
        upload_to=("profiles/%y/%m/%d/"), default="customer-default.png"
    )
    # STATUS_CHOICES= (('GUEST','Guest'), ('PREMIUM','PREMIUM'),('NORMAL','NORMAL'))#comme constant

    perferances = models.TextField(blank=True)
    search_history = models.TextField(blank=True)
    background = models.TextField(blank=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    is_month_customer = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.owner.username}"

    class Status(models.TextChoices):
        GUEST = "Guest"
        PREMIUM = "PREMIUM"
        NORMAL = "Normal"

    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.NORMAL
    )


class RealtorProfile(models.Model):
    phone = models.CharField(max_length=50, blank=True)
    profile_image = models.ImageField(
        upload_to="realtors/%Y/%m/%d/", default="realtor-default.png"
    )
    biographie = models.TextField(blank=True)
    is_seller_of_month = models.BooleanField(default=False)
    affiliation_date = models.DateField(auto_now=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:  # pour acceder a son nom donner
        return f"{self.owner.username}"


class DesignerProfile(models.Model):
    phone = models.CharField(max_length=50, blank=True)
    portfolio_url = models.URLField(blank=True)
    skills = models.TextField(blank=True)  # Store skills as comma-separated values
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(
        upload_to="designers/%Y/%m/%d/", default="designer-default.png"
    )
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.owner.username}"
