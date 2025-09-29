from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Candidate, Representative, Party
from django.contrib.auth.models import User, Group, Permission
import os

@receiver(post_save, sender=User)
def create_mod_grp_and_assign(sender, instance, created, **kwargs):
    if instance.is_superuser: return
    if not instance.is_staff: return
    mod_group, created = Group.objects.get_or_create(name='mod')
    if created:
        codenames = ['add_candidate', 'change_candidate', 'delete_candidate', 'view_candidate', 'add_case', 'change_case', 'delete_case', 'view_case', 'add_kartut', 'change_kartut', 'delete_kartut', 'view_kartut', 'view_party', 'add_representative', 'change_representative', 'delete_representative', 'view_representative', 'view_user', 'view_district', 'view_municipality']
        perms = Permission.objects.filter(codename__in=codenames)
        mod_group.permissions.set(perms)
    instance.groups.add(mod_group)

def cleanup_file_on_change(sender, instance, field_name: str):
    """Remove old file if a FileField/ImageField changes."""
    if not instance.id:
        return
    try:
        previous = sender.objects.get(id=instance.id)
    except sender.DoesNotExist:
        return

    old_file = getattr(previous, field_name)
    new_file = getattr(instance, field_name)
    if old_file and old_file != new_file and hasattr(old_file, 'path') and os.path.isfile(old_file.path):
        os.remove(old_file.path)

def cleanup_file_on_delete(instance, field_name: str):
    """Remove file from filesystem when object is deleted."""
    file_field = getattr(instance, field_name)
    if file_field and hasattr(file_field, 'path') and os.path.isfile(file_field.path):
        os.remove(file_field.path)

@receiver(pre_save, sender=Candidate)
def candidate_pre_save(sender, instance, **kwargs):
    cleanup_file_on_change(sender, instance, "image")

@receiver(post_delete, sender=Candidate)
def candidate_post_delete(sender, instance, **kwargs):    
    cleanup_file_on_delete(instance, "image")   

@receiver(pre_save, sender=Party)
def party_pre_save(sender, instance, **kwargs):
    cleanup_file_on_change(sender, instance, "flag")

@receiver(post_delete, sender=Party)
def party_post_delete(sender, instance, **kwargs):    
    cleanup_file_on_delete(instance, "flag")  

@receiver(pre_save, sender=Representative)
def representative_pre_save(sender, instance, **kwargs):
    cleanup_file_on_change(sender, instance, "symbol")

@receiver(post_delete, sender=Representative)
def representative_post_delete(sender, instance, **kwargs):    
    cleanup_file_on_delete(instance, "symbol")
