from django.contrib import admin
from  contact.models import *
from  .models import Feedback
# Register your models here.
admin.site.register(Order)
admin.site.register(Feedback)