import os.path

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from mysite import settings

from PIL import ImageEnhance, Image

from mysite.settings import BASE_DIR


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


@receiver(post_save, sender=User)
def add_watermark(sender, instance=None, created=False, **kwargs):
    image_path = instance.photo.path

    # todo change then add static root
    watermark_path = os.path.join(BASE_DIR, 'media/Watermark_Logo.jpg')
    opacity = 0.25
    wm_interval = 0

    image = Image.open(image_path)
    watermark = Image.open(watermark_path)

    if watermark.mode != 'RGBA':
        watermark = watermark.convert('RGBA')
    else:
        watermark = watermark.copy()
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    watermark.putalpha(alpha)

    layer = Image.new('RGBA', image.size, (0, 0, 0, 0))

    for y in range(0, image.size[1], watermark.size[1] + wm_interval):
        for x in range(0, image.size[0], watermark.size[0] + wm_interval):
            layer.paste(watermark, (x, y))

    Image.composite(layer, image, layer).save(image_path)
