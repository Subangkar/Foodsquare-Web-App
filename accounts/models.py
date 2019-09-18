import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from browse.utils import distance


class User(AbstractUser):
	"""User's login credential entity for any system user"""
	is_customer = models.BooleanField('Customer Account', default=False)
	is_manager = models.BooleanField('Manager Account', default=False)
	is_branch_manager = models.BooleanField('Branch Manager Account', default=False)
	is_delivery_man = models.BooleanField('Delivery Account', default=False)
	backend = 'django.contrib.auth.backends.ModelBackend'

	is_suspended = models.BooleanField('Suspended Account', default=False)

	class Meta:
		verbose_name = "User"
		verbose_name_plural = "Users"

	def get_rating(self):
		rating = 0
		if self.is_customer:
			from customer.utils_db import get_avg_customer_rating
			rating = get_avg_customer_rating(self.id)
		elif self.is_delivery_man:
			from delivery.utils_db import get_avg_deliveryman_rating
			rating = get_avg_deliveryman_rating(self.id)
		elif self.is_manager:
			rating = self.restaurant.get_avg_rating()
		elif self.is_branch_manager:
			rating = self.restaurantbranch.get_avg_rating()
		if rating is None:
			rating = 0
		return round(rating, 2)

	def get_unread_notifications(self):
		from customer.models import Notification
		return Notification.get_unread_notifications(self)

	def read_notifications(self, time):
		from customer.models import Notification
		for notf in Notification.objects.filter(user=self, time__lte=time):
			notf.mark_as_read()

	def suspend_account(self):
		self.is_suspended = True
		self.save()
		self.send_mail(
			subject='Account Deactivated',
			message='Your account has been deactivated for bad reputation.\n ' +
			        'We are verifying your account.\n ' +
			        'You will be mailed via this email when we are done.'
		)
		from customer.utils_db import send_notification
		if self.is_customer:
			send_notification(self.id,
			                  "Your account has been suspended due to lower rating. You cannot order any items until you contact us.")
		elif self.is_delivery_man:
			send_notification(self.id,
			                  "Your account has been suspended due to lower rating. You cannot accept any delivery until you contact us")

	def active_account(self):
		self.is_suspended = False
		self.save()
		self.send_mail(
			subject='Account Activated',
			message='Your account has been reactivated.\n ')
		from customer.utils_db import send_notification
		send_notification(self.id, "Welcome Back, " + self.username)

	def get_order_count(self):
		"""
		:return: current month's delivered orders count
		"""
		from django.utils.timezone import datetime
		today = datetime.today()
		if self.is_customer:
			return Order.objects.filter(user=self, order_status__in=[Order.DELIVERED],
			                            time__month=today.month, time__year=today.year).count()
		if self.is_delivery_man:
			return Order.objects.filter(delivery__deliveryman__user=self, order_status__in=[Order.DELIVERED],
			                            time__month=today.month, time__year=today.year).count()
		if self.is_manager:
			return Order.objects.filter(branch__restaurant=self.restaurant, order_status__in=[Order.DELIVERED],
			                            time__month=today.month, time__year=today.year).count()
		if self.is_branch_manager:
			return Order.objects.filter(branch=self.restaurantbranch, order_status__in=[Order.DELIVERED],
			                            time__month=today.month, time__year=today.year).count()
		return 0

	def get_image(self):
		if self.is_customer:
			return self.userprofile.avatar
		if self.is_manager:
			return self.restaurant.get_image()
		if self.is_branch_manager:
			return self.restaurantbranch.get_image()
		return 'default.png'

	def send_mail(self, subject, message, from_email='admin@foodsquare'):
		print('sending mail to', self)
		import django.core.mail
		django.core.mail.send_mail(
			subject=subject,
			message='Username:' + self.username + '\n ' + 'Email:' + self.email + '\n ' + message,
			from_email=from_email,
			recipient_list=[self.email],
			fail_silently=False,
		)

	def get_suspend_contact_email(self):
		from webAdmin.models import Config
		return Config.get_value(Config.ACCOUNT_SUSPEND_CONTACT)


class UserProfile(models.Model):
	"""Customer profile entity"""
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=20, null=True)
	last_name = models.CharField(max_length=20, null=True)
	address = models.TextField(max_length=150, null=True)
	avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')

	def __str__(self):
		return str(self.first_name or None) + str(self.last_name or None) + self.user.username + " " + str(
			self.address or None) + str(self.avatar.url)


class Restaurant(models.Model):
	"""Restaurant Profile Entity"""
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	restaurant_name = models.CharField(max_length=50, blank=False, null=False)
	restaurant_key = models.CharField(max_length=250, default='0')
	trade_license = models.CharField(max_length=50, unique=True, blank=False)

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

	def get_image(self):
		return self.restaurantImg


class RestaurantBranch(models.Model):
	"""Branch Profile Entity"""
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

	image = models.ImageField(upload_to='restaurant_img/', default='restaurant_img/default.png')

	running = models.BooleanField(default=False)
	opening_time = models.FloatField(verbose_name='Opening Time in 24h format', default=9.00)
	closing_time = models.FloatField(verbose_name='Opening Time in 24h format', default=23.00)

	# branch_contact_info = models.ForeignKey(ContactInfo, on_delete=models.CASCADE)

	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

	ratings = models.ManyToManyField(User, through='browse.BranchRating', related_name='branch_rating_user')
	comments = models.ManyToManyField(User, through='browse.BranchComment', related_name='branch_comment_user')

	MAX_DELIVERABLE_DISTANCE = 4

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

	def get_image(self):
		if self.image == 'restaurant_img/default.png':
			return self.restaurant.get_image()
		return self.image


class Payment(models.Model):
	"""Payment log entity for any order"""
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
	"""Deliveryman Profile Entity"""
	name = models.CharField(verbose_name="Name", max_length=50)
	contactNum = models.CharField(verbose_name="Phone Number", max_length=15)
	address = models.CharField(verbose_name="Delivery Address", max_length=50)
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
	"""Delivery log entity for any order"""
	address = models.CharField(verbose_name="Delivery Address Description", max_length=50)
	address_desc = models.CharField(verbose_name="Delivery Address Description", max_length=50)
	location = models.CharField(verbose_name='Coordinate of Delivery Location', max_length=50, default='0,0')
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

	def address_flat_no(self):
		return self.address_desc.split(',')[0]

	def address_house_no(self):
		return self.address_desc.split(',')[1]

	def address_road_no(self):
		return self.address_desc.split(',')[2]

	def address_block(self):
		return self.address_desc.split(',')[3]

	def address_area(self):
		return self.address


class Order(models.Model):
	"""Order log entity"""
	time = models.DateTimeField(verbose_name="Order Place Time", auto_now_add=False)

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
		return self.user.username + ' ' + self.time.__repr__() + ' ' + self.payment.__repr__()

	def get_package_list(self):
		return OrderPackageList.objects.filter(order=self)

	def assignDeliveryman(self, deliveryman):
		self.order_status = Order.DELIVERING
		self.delivery.deliveryman = deliveryman
		self.delivery.charge = self.payment.price - sum(pack.price for pack in self.get_package_list())
		self.delivery.save()
		self.save()

	def submitDelivery(self):
		self.order_status = Order.DELIVERED
		self.payment.payment_status = Payment.PAID
		self.payment.save()
		self.save()


class OrderPackageList(models.Model):
	"""Keeps Track of cuisines in any Order"""
	order = models.ForeignKey("accounts.Order", verbose_name="Order", on_delete=models.CASCADE)
	package = models.ForeignKey("browse.Package", verbose_name="Package", on_delete=models.CASCADE)
	quantity = models.IntegerField(verbose_name="#Packages in this order", default=1)
	price = models.FloatField(verbose_name="Total Price of all items for this package considering offer", default=0)

	class Meta:
		verbose_name = "OrderPackageList"
		verbose_name_plural = "OrderPackageLists"

	def __str__(self):
		return ''.join(self.package.pkg_name)

	def get_absolute_url(self):
		return reverse("OrderPackageList_detail", kwargs={"pk": self.pk})


# --------------------- Signals / Triggers --------------------------


@receiver(post_save, sender=Delivery, dispatch_uid="update_order_status")
def update_suspend_status(sender, instance, **kwargs):
	"""
	Checks on rating submit whether ratings of any customer/deliveryman has fallen below 2.00 to suspend that account.
	"""
	print('delivery saved/updated ', instance)
	if not Order.objects.filter(delivery=instance).exists():
		return
	order = Order.objects.get(delivery=instance)
	if order.order_status in [Order.DELIVERING, Order.DELIVERED]:
		if 0 < order.user.get_rating() < 2.00:
			order.user.suspend_account()
			print(instance.user, " suspended !!!")
		if 0 < order.delivery.deliveryman.user.get_rating() < 2.00:
			order.delivery.deliveryman.user.suspend_account()
			print(order.delivery.deliveryman.user, " suspended !!!")
