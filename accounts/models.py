from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


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
		return self.restaurant_name + " "

	def get_absolute_url(self):
		return reverse("Restaurant_detail", kwargs={"id": self.pk})


class RestaurantBranch(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	branch_name = models.CharField(blank=False, null=False, max_length=50)
	branch_location = models.CharField("Openstreetmap co-ordinates", max_length=50, default='0,0')
	branch_location_details = models.CharField("If co-ordinates can't be provided or floor-no", max_length=100, default='')
	location_area =  models.CharField(default='', max_length=50)
	branch_phonenum = models.CharField(max_length=20, default='')
	branch_mobilenum = models.CharField(max_length=20, default='')
	branch_email = models.CharField(max_length=50, default='')

	# branch_contact_info = models.ForeignKey(ContactInfo, on_delete=models.CASCADE)

	restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

	# branch_location = LocationField(based_fields=['city'], zoom=7, default=Point(1.0, 1.0)) # https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/postgis/

	# branch_location = PlainLocationField() # https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/postgis/
	class Meta:
		verbose_name = "Branch"
		verbose_name_plural = "Branches"

	def __str__(self):
		return self.branch_name

	def get_absolute_url(self):
		return reverse("Branch_detail", kwargs={"pk": self.pk})


class Payment(models.Model):

	CASH = 'C'
	ONLINE = 'O'
	PAYMENT_TYPES = (
        (CASH, 'Cash'),
        (ONLINE, 'Online'),
    )

	price = models.FloatField(("Total Price"))
	payment_type = models.CharField(("Payment Type"), max_length=1, choices=PAYMENT_TYPES, default=CASH)

	class Meta:
		verbose_name = ("Payment")
		verbose_name_plural = ("Payments")

	def __str__(self):
		return self.price + " " + self.payment_type

	def get_absolute_url(self):
		return reverse("Payment_detail", kwargs={"pk": self.pk})



class DeliveryMan(models.Model):

	name = models.CharField(("Name"), max_length=50)
	contactNum = models.CharField(("Phone Number"), max_length=15)
	address = models.CharField(("Permanent Address"), max_length=50)
	nid = models.CharField(("National ID No."), max_length=50)

	class Meta:
		verbose_name = ("DeliveryMan")
		verbose_name_plural = ("DeliveryMen")

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("DeliveryMan_detail", kwargs={"pk": self.pk})


class Delivery(models.Model):

	address = models.CharField(("Delivery Address Description"), max_length=50)
	address_desc = models.CharField(("Delivery Address Description"), max_length=50)
	charge = models.FloatField(("Delivery Fees"))
	time = models.DateTimeField(("Delivery Completion Time"), auto_now=False, auto_now_add=False)
	rating_user = models.IntegerField(("User Rating"))
	rating_deliveryman = models.IntegerField(("Delivery Man Rating"))

	deliveryman = models.ForeignKey(DeliveryMan, verbose_name=(""), on_delete=models.CASCADE)

	class Meta:
		verbose_name = ("Delivery")
		verbose_name_plural = ("Deliveries")

	def __str__(self):
		return 'self.name'

	def get_absolute_url(self):
		return reverse("Delivery_detail", kwargs={"pk": self.pk})


class Order(models.Model):

	time = models.DateTimeField(("Order Place Time"), auto_now=False, auto_now_add=False)

	user = models.ForeignKey(User, verbose_name=("Person To Deliver"), on_delete=models.CASCADE)
	delivery = models.ForeignKey(Delivery, verbose_name=("Person To Deliver"), on_delete=models.CASCADE)
	payment = models.ForeignKey(Payment, verbose_name=("Person To Deliver"), on_delete=models.CASCADE)

	pkg_list = models.ManyToManyField("browse.Package", through='OrderPackageList', verbose_name=("Packages in Order"))

	class Meta:
		verbose_name = ("Order")
		verbose_name_plural = ("Orders")

	def __str__(self):
		return 'self.name'

	def get_absolute_url(self):
		return reverse("Order_detail", kwargs={"pk": self.pk})


class OrderPackageList(models.Model):
	
	order = models.ForeignKey("accounts.Order", verbose_name=("Order"), on_delete=models.CASCADE)
	delivery = models.ForeignKey("browse.Package", verbose_name=("Package"), on_delete=models.CASCADE)

	class Meta:
		verbose_name = ("OrderPackageList")
		verbose_name_plural = ("OrderPackageLists")

	def __str__(self):
		return 'self.name'

	def get_absolute_url(self):
		return reverse("OrderPackageList_detail", kwargs={"pk": self.pk})
