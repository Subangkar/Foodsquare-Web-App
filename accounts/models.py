from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
# from location_field.models.spatial import LocationField
from django.urls import reverse
from location_field.models.plain import PlainLocationField


class User(AbstractUser):
	is_customer = models.BooleanField('Customer Account', default=False)
	is_manager = models.BooleanField('Manager Account', default=False)

	backend = 'django.contrib.auth.backends.ModelBackend'

	class Meta:
		verbose_name = "User"
		verbose_name_plural = "Users"


# user contactinfo not completed
class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=20, null=True)
	last_name = models.CharField(max_length=20, null=True)
	address = models.TextField(max_length=150, null=True)
	avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')

	def __str__(self):
		return str(self.first_name or None) + str(self.last_name or None) + self.user.username + " " + str(
			self.address or None) + str(self.avatar.url)


class Restaurant(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	restaurant_name = models.CharField(max_length=50, blank=False, null=False)
	restaurant_key = models.CharField(max_length=250, default='0')
	trade_license = models.CharField(max_length=50, unique=True, blank=False)

	# ei field ta
	restaurantImg = models.ImageField(upload_to='restaurant_img/', default='restaurant_img/default.png')

	class Meta:
		verbose_name = "Restaurant"
		verbose_name_plural = "Restaurants"

	def __str__(self):
		return self.restaurant_name + " " + self.restaurantImg.url

	def get_absolute_url(self):
		return reverse("Restaurant_detail", kwargs={"id": self.pk})


class ContactInfo(models.Model):
	phone = models.CharField(max_length=20)
	mobile = models.CharField(max_length=20)
	email = models.EmailField(max_length=254)

	class Meta:
		verbose_name = "ContactInfo"
		verbose_name_plural = "ContactInfos"

	def __str__(self):
		return self.mobile

	def get_absolute_url(self):
		return reverse("ContactInfo_detail", kwargs={"pk": self.pk})


class RestaurantBranch(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	branch_name = models.CharField(blank=False, null=False, max_length=50)
	branch_location = PlainLocationField(based_fields=['city'], zoom=7)

	branch_contact_info = models.ForeignKey(ContactInfo, on_delete=models.CASCADE)

	restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

	# branch_location = LocationField(based_fields=['city'], zoom=7, default=Point(1.0, 1.0)) # https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/postgis/

	class Meta:
		verbose_name = "Branch"
		verbose_name_plural = "Branches"

	def __str__(self):
		return self.branch_name

	def get_absolute_url(self):
		return reverse("Branch_detail", kwargs={"pk": self.pk})

