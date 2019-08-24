import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from browse.utils import distance


class User(AbstractUser):
	is_customer = models.BooleanField('Customer Account', default=False)
	is_manager = models.BooleanField('Manager Account', default=False)
	is_branch_manager = models.BooleanField('Branch Manager Account', default=False)
	is_delivery_man = models.BooleanField('Delivery Account', default=False)
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
		return reverse("browse:restaurant_detail", kwargs={"id": self.pk})

	def get_avg_rating(self):
		from browse.utils_db import get_rating_restaurant
		return get_rating_restaurant(self.id)


class RestaurantBranch(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	branch_name = models.CharField(blank=False, null=False, max_length=50)
	branch_location = models.CharField(verbose_name="Openstreetmap co-ordinates", max_length=50, default='0,0')
	branch_location_details = models.CharField(verbose_name="If co-ordinates can't be provided or floor-no",
	                                           max_length=100,
	                                           default='')
	location_area = models.CharField(default='', max_length=50)
	branch_phonenum = models.CharField(max_length=20, default='')
	branch_mobilenum = models.CharField(max_length=20, default='')
	branch_email = models.CharField(max_length=50, default='')

	running = models.BooleanField(default=False)
	opening_time = models.FloatField(verbose_name='Opening Time in 24h format', default=9.00)
	closing_time = models.FloatField(verbose_name='Opening Time in 24h format', default=23.00)
	# opening_time = models.DateTimeField(verbose_name='Opening Time in 24h format', default=datetime.now())
	# closing_time = models.DateTimeField(verbose_name='Opening Time in 24h format', default=23.00)

	# branch_contact_info = models.ForeignKey(ContactInfo, on_delete=models.CASCADE)

	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

	ratings = models.ManyToManyField(User, through='browse.BranchRating', related_name='branch_rating_user')
	comments = models.ManyToManyField(User, through='browse.BranchComment', related_name='branch_comment_user')

	class Meta:
		verbose_name = "Branch"
		verbose_name_plural = "Branches"

	def __str__(self):
		return self.branch_name

	def get_absolute_url(self):
		return reverse("browse:Branch_detail", kwargs={"id": self.pk})

	def is_open_now(self):
		time_now = datetime.datetime.now().time().hour + datetime.datetime.now().time().minute / 60
		return self.opening_time <= time_now <= self.closing_time and self.running

	def distance(self, coordinates):
		return distance(self.branch_location, coordinates)

	def get_avg_rating(self):
		from browse.utils_db import get_rating_branch
		return get_rating_branch(self.id)


class Payment(models.Model):
	CASH = 'C'
	ONLINE = 'O'
	PAYMENT_TYPES = (
		(CASH, 'Cash'),
		(ONLINE, 'Online'),
	)

	PAID = 'P'
	DUE = 'D'
	PAYMENT_STATUS = (
		(PAID, 'Paid'),
		(DUE, 'Due'),
	)

	price = models.FloatField(verbose_name="Total Price")
	payment_type = models.CharField(verbose_name="Payment Type", max_length=1, choices=PAYMENT_TYPES, default=CASH)
	payment_status = models.CharField(verbose_name="Payment Status", max_length=1, choices=PAYMENT_STATUS, default=DUE)
	bkash_ref = models.CharField(verbose_name="Bkash ref", max_length=30, null=True, blank=True)

	class Meta:
		verbose_name = "Payment"
		verbose_name_plural = "Payments"

	def __str__(self):
		return str(self.price) + " " + self.payment_type

	def get_absolute_url(self):
		return reverse("Payment_detail", kwargs={"pk": self.pk})


class DeliveryMan(models.Model):
	name = models.CharField(verbose_name="Name", max_length=50)
	contactNum = models.CharField(verbose_name="Phone Number", max_length=15)
	address = models.CharField(verbose_name="Permanent Address", max_length=50)
	nid = models.CharField(verbose_name="National ID No.", max_length=50)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')

	class Meta:
		verbose_name = "DeliveryMan"
		verbose_name_plural = "DeliveryMen"

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("DeliveryMan_detail", kwargs={"pk": self.pk})


class Delivery(models.Model):
	address = models.CharField(verbose_name="Delivery Address Description", max_length=50)
	address_desc = models.CharField(verbose_name="Delivery Address Description", max_length=50)
	charge = models.FloatField(verbose_name="Delivery Fees", default=50)
	time = models.DateTimeField(verbose_name="Delivery Completion Time", auto_now=True, auto_now_add=False)
	rating_user = models.IntegerField(verbose_name="User Rating", null=True)
	rating_deliveryman = models.IntegerField(verbose_name="Delivery Man Rating", null=True)

	deliveryman = models.ForeignKey(DeliveryMan, verbose_name="Delivery Man", on_delete=models.CASCADE, null=True)

	class Meta:
		verbose_name = "Delivery"
		verbose_name_plural = "Deliveries"

	def __str__(self):
		return 'self.name'

	def get_absolute_url(self):
		return reverse("Delivery_detail", kwargs={"pk": self.pk})


class Order(models.Model):
	time = models.DateTimeField(verbose_name="Order Place Time", auto_now=True, auto_now_add=False)

	user = models.ForeignKey(User, verbose_name="Person To Deliver", on_delete=models.CASCADE, null=False, blank=False)
	delivery = models.ForeignKey(Delivery, verbose_name="Delivery Info", on_delete=models.CASCADE, null=True,
	                             blank=True)
	payment = models.ForeignKey(Payment, verbose_name="Payment Info", on_delete=models.CASCADE, null=True, blank=True)
	branch = models.ForeignKey(RestaurantBranch, verbose_name="Branch", on_delete=models.CASCADE, null=False,
	                           blank=False)

	pkg_list = models.ManyToManyField("browse.Package", through='OrderPackageList', verbose_name="Packages in Order")

	# houseNo = models.CharField(verbose_name="Delivery House No")
	mobileNo = models.CharField(verbose_name="Mobile Number", max_length=15, null=False, blank=False, default='0')
	# status = models.CharField(verbose_name="Order Status", max_length=15, null=False, default='Pending')

	PENDING = 'PENDING'
	PROCESSING = 'PROCESSING'
	DELIVERING = 'DELIVERING'
	DELIVERED = 'DELIVERED'
	ORDER_STATUS = (
		(PENDING, 'PENDING'),
		(PROCESSING, 'PROCESSING'),
		(PROCESSING, 'DELIVERING'),
		(DELIVERED, 'DELIVERED')
	)

	order_status = models.CharField(verbose_name="Order Status", max_length=15, choices=ORDER_STATUS, default=PENDING)

	class Meta:
		verbose_name = "Order"
		verbose_name_plural = "Orders"

	def __str__(self):
		return self.user.username + ' ' + self.time.__repr__() + ' ' + self.payment

	def get_package_list(self):
		return OrderPackageList.objects.filter(order=self)


class OrderPackageList(models.Model):
	order = models.ForeignKey("accounts.Order", verbose_name="Order", on_delete=models.CASCADE)
	package = models.ForeignKey("browse.Package", verbose_name="Package", on_delete=models.CASCADE)
	quantity = models.IntegerField(verbose_name="#Packages in this order", default=1)

	class Meta:
		verbose_name = "OrderPackageList"
		verbose_name_plural = "OrderPackageLists"

	def __str__(self):
		return ''.join(self.package.pkg_name)

	def get_absolute_url(self):
		return reverse("OrderPackageList_detail", kwargs={"pk": self.pk})
