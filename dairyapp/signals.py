from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    for role in ['Admin', 'Staff', 'Worker', 'Customer']:
        Group.objects.get_or_create(name=role)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'userprofile'):
        # You can skip automatic profile creation if not needed
        pass
