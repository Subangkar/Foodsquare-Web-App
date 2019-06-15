from django.contrib.auth.models import User
from django.db import models


class Menu(models.Model):
	menu_name = models.CharField(max_length=140, blank=True)
	price = models.IntegerField()
	menu_img = models.ImageField(upload_to='menu/', default='avatars/default.png')
