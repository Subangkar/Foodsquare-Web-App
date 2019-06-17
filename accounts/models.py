from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=20, null=True)
	last_name = models.CharField(max_length=20, null=True)
	address = models.TextField(max_length=150, null=True)
	avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')

	def __str__(self):
		return str(self.first_name or None) + str(self.last_name or None) + self.user.username+" "+str(self.address or None)


class RestaurantProfile(models.Model):
	age = models.IntegerField(default=0)
	avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')