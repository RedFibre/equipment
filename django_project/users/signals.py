from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from equ.models import Lab,UserLab

User = get_user_model()

@receiver(post_save, sender=User)
def assign_to_labuser_group(sender, instance, created, **kwargs):
    if created:
        labuser_group = Group.objects.get(name='labuser')
        instance.groups.add(labuser_group)

@receiver(post_save, sender=User)
def create_user_lab(sender, instance, created, **kwargs):
    if created:
        lab_id = instance.username[:3]  # Extract the first 3 digits from the username
        try:
            lab = Lab.objects.get(name=lab_id)  # Query the Lab model to find the matching lab
            UserLab.objects.create(user=instance, lab=lab)  # Create a UserLab instance with the user and lab
        except Lab.DoesNotExist:
            pass

