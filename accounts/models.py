from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    Extends the built-in User model with additional profile information.

    Each user has a one-to-one relationship with a Profile.
    Stores optional bio and avatar image for the user.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    bio = models.TextField(
        blank=True,
        null=True
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        default='avatars/default.png'
    )

    def __str__(self):
        """
        Returns a string representation of the profile.
        """
        return f"{self.user.username}'s profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver that creates a Profile instance
    whenever a new User is created.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal receiver that saves the associated Profile
    whenever a User instance is saved.
    """
    instance.profile.save()
