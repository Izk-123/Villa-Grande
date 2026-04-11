from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

class Permission(models.Model):
    """System permission – each is identified by a unique code."""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Role(models.Model):
    """Role with a set of permissions."""
    name = models.CharField(max_length=50)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    """Extension of the User model for role and permissions."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.user.username} - {self.role.name if self.role else 'No role'}"

# Automatically create a UserProfile whenever a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
@receiver(post_save, sender=User)
def ensure_user_profile(sender, instance, **kwargs):
    """Create or update a profile for every user."""
    UserProfile.objects.get_or_create(user=instance)