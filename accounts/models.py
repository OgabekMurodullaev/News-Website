from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user/', blank=True, null=True)
    day_of_birth = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}'

    objects = models.Manager()
