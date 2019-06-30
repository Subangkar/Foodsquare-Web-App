# from django.contrib.auth.models import User
from django.db import models


class Menu(models.Model):
	menu_name = models.CharField(max_length=140, blank=True)
	price = models.IntegerField()
	menu_img = models.ImageField(upload_to='menu/', default='avatars/default.png')


# class RestaurantPendingReq(models.Model):

# 	rest_name = models.CharField(max_length=50)
# 	user_name = models.CharField(max_length=50)
# 	password = models.CharField(max_length=50)
# 	email = models.EmailField(max_length=254)
# 	trade_license = models.CharField(max_length=50)

# 	class Meta:
# 		verbose_name = ("RestaurantPendingRequest")
# 		verbose_name_plural = ("RestaurantPendingRequests")

# 	def __str__(self):
# 		return self.name

# 	def get_absolute_url(self):
# 		return reverse("RestaurantPendingReq_detail", kwargs={"pk": self.pk})
