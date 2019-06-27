from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
# from location_field.models.spatial import LocationField
from django.urls import reverse
from location_field.models.plain import PlainLocationField
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone


class User(AbstractUser):
	is_customer = models.BooleanField(default=False)
	is_manager = models.BooleanField(default=False)

	class Meta:
		verbose_name = "User"
		verbose_name_plural = "Users"

# user_id = models.CharField(max_length=50, unique=True)
# email = models.EmailField(max_length=254, unique=True)
# CUSTOMER = 'C'
# MANAGER = 'M'
# ADMIN = 'A'
# USER_TYPE_CHOICES = [
# 	(CUSTOMER, 'Customer'),
# 	(MANAGER, 'Manager'),
# 	(ADMIN, 'Admin'),
# ]
# user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default=CUSTOMER)
# date_joined = models.DateTimeField(('date joined'), default=timezone.now)
# is_staff = models.BooleanField(('staff status'), default=False,
#                                help_text=('Determines if user can access the admin site'))
# USERNAME_FIELD = 'user_id'
# REQUIRED_FIELDS = ['user_id', 'email']


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

# pass


# class CustomUserManager(BaseUserManager):
# 	def create_user(self, email, first_name, last_name, password=None,
# 	                **extra_fields):
# 		'''
# 		Create a CustomUser with email, name, password and other extra fields
# 		'''
# 		now = timezone.now()
# 		if not email:
# 			raise ValueError('The email is required to create this user')
# 		email = CustomUserManager.normalize_email(email)
# 		cuser = self.model(user_id=,email=email, first_name=first_name,
# 		                   last_name=last_name, is_staff=False,
# 		                   is_active=True, is_superuser=False,
# 		                   date_joined=now, last_login=now, **extra_fields)
# 		cuser.set_password(password)
# 		cuser.save(using=self._db)
# 		return cuser
#
# 	def create_superuser(self, email, first_name, last_name, password=None,
# 	                     **extra_fields):
# 		u = self.create_user(email, first_name, last_name, password,
# 		                     **extra_fields)
# 		u.is_staff = True
# 		u.is_active = True
# 		u.is_superuser = True
# 		u.save(using=self._db)
#
# 		return u
