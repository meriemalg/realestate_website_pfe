from django.contrib import admin
from .models import *


class RealtorProfileAdmin(admin.ModelAdmin):
    list_display = ["profile_image", "owner"]
    list_display_links = ["owner"]  # pour faire link
    search_fields = ["owner"]  # chercher a l aide user
    list_filter = ["owner"]


class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ["profile_image", "owner"]
    list_display_links = ["owner"]  # pour faire link
    search_fields = ["owner"]  # chercher a l aide user
    list_filter = ["owner"]


class DesignerProfileAdmin(admin.ModelAdmin):
    list_display = ["profile_image", "owner"]
    list_display_links = ["owner"]  # pour faire link
    search_fields = ["owner"]  # chercher a l aide user
    list_filter = ["owner"]


# Register your models here.
admin.site.register(RealtorProfile, RealtorProfileAdmin)
admin.site.register(DesignerProfile, DesignerProfileAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin)
