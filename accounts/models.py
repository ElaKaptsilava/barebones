import os
from PIL import Image

from django.contrib.auth.models import AbstractUser
from django.db import models


def user_directory_path(instance, filename):
    return f'user_{instance.pk}_{instance.username}_{instance.last_name}/{filename}'


class CustomUser(AbstractUser):
    class Gender(models.TextChoices):
        female = 'Female'
        male = 'Male'
        other = 'Other'

    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=10)
    gender = models.CharField(max_length=10, choices=Gender.choices, default=Gender.male)
    image = models.ImageField(upload_to=user_directory_path, default='default_user.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'native_name', 'phone_no']

    def __str__(self):
        return "{}".format(self.email)

    def __repr__(self):
        return f"CustomUser('{self.email}', '{self.username}, {self.last_name}"

    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
