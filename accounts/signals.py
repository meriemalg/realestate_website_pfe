from .models import *
from django.contrib.auth.models import User
from django.dispatch import receiver


from django.db.models.signals import m2m_changed


@receiver(m2m_changed, sender=User.groups.through)
def update_user_profiles(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove"]:
        user_groups = instance.groups.values_list("name", flat=True)

        if "designer" in user_groups:
            DesignerProfile.objects.get_or_create(owner=instance)
            print(f"Designer profile checked for user {instance.username}")
        if "realtor" in user_groups:
            RealtorProfile.objects.get_or_create(owner=instance)
            print(f"Realtor profile checked for user {instance.username}")
        if "customer" in user_groups:
            CustomerProfile.objects.get_or_create(owner=instance)
            print(f"Customer profile checked for user {instance.username}")
