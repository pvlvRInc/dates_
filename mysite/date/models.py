from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from mysite import settings


class User(AbstractUser):
    photo = models.ImageField(upload_to='media/%Y/%m/%d')
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(pre_delete, sender=User)
def delete_image_file(sender, instance=None, created=False, **kwargs):
    storage, path = instance.photo.storage, instance.photo.path
    storage.delete(path)
