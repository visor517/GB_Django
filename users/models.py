import pytz
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True)

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def is_activation_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) < (self.activation_key_created + timedelta(hours=48)):
            return False
        return True


class UserExtention(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, db_index=True)
    tagline = models.CharField(max_length=150, blank=True, verbose_name='теги')
    about_me = models.TextField(blank=True, verbose_name='о себе')
    gender = models.CharField(choices=GENDER_CHOICES, blank=True, max_length=1, verbose_name='пол')
    age = models.DateField(blank=True, null=True, verbose_name='возраст')

    @receiver(post_save, sender=User)
    def create_user_extention(sender, instance, created, **kwargs):
        if created:
            UserExtention.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_extention(sender, instance, **kwargs):
        instance.userextention.save()
