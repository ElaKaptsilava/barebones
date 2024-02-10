import csv
import os

from PIL import Image

from django.contrib.auth.models import AbstractUser
from django.db import models


def user_directory_path(instance, filename):
    return f'user_{instance.email}_{instance.last_name}/{filename}'


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
        return f"CustomUser('{self.email}', '{self.username}, {self.last_name})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
        self.write_user_profile_to_file()

    def write_user_profile_to_file(self): # 2 func
        file_path = "users.csv"
        header = ["email", "username", "password"]
        user_info = [self.email, self.username, self.password]

        with open(file_path, "a", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            if os.path.getsize(file_path) == 0:
                csvwriter.writerow(header)
                users = CustomUser.objects.all()
                get_users = [[user.email, user.username, user.password] for user in users]
                csvwriter.writerows(get_users)
            else:
                csvwriter.writerow(user_info)
