from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	desc = models.CharField(max_length=140, blank=True)
	age = models.IntegerField(default=0)
	avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')


class RestaurantProfile(models.Model):
	age = models.IntegerField(default=0)
	avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')