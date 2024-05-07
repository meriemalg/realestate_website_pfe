
from . import views
from django.urls import path
from .models import Order
urlpatterns = [
   path("contact",views.contact,name="contact"),
   path("order",views.order,name="order")
]