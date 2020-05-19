from django.db import models
from django.urls import reverse

from accounts.models import Restaurant, User, RestaurantBranch


class Ingredient(models.Model):
	"""Raw ingredients of a cuisine like chicken, bun etc."""
	name = models.CharField(max_length=50)

	class Meta:
		verbose_name = "Ingredient"
		verbose_name_plural = "Ingredients"

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("Ingredient_detail", kwargs={"pk": self.pk})


class Package(models.Model):
	"""
	Entity for a cuisine maintained by a restaurant
	"""
	pkg_name = models.CharField(max_length=50)
	for_n_persons = models.IntegerField(default=1, null=False)
	price = models.IntegerField(blank=False, null=False)
	available = models.BooleanField(default=True)
	image = models.ImageField(upload_to='menu/', default='menu/default.png')
	details = models.CharField(max_length=250, blank=True)
	category = models.CharField(max_length=50)
	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

	ingr_list = models.ManyToManyField(Ingredient, through='IngredientList')

	ratings = models.ManyToManyField(User, through='PackageRating', related_name='package_rating_user')
	comments = models.ManyToManyField(User, through='PackageComment', related_name='package_comment_user')

	branch_details = models.ManyToManyField('accounts.RestaurantBranch', through='PackageBranchDetails',
	                                        related_name='branch_details')

	is_vegeterian = models.BooleanField(verbose_name='is only a vegetable item', default=False)

	class Meta:
		verbose_name = "Package"
		verbose_name_plural = "Packages"

	def __str__(self):
		return self.pkg_name

	def get_absolute_url(self):
		return reverse("browse:package-details", kwargs={"id": self.pk})

	def get_absolute_edit_url(self):
		return reverse("manager:edit_menu", kwargs={"id": self.pk})

	def is_editable(self, user):
		return user.is_authenticated and user.is_manager and user.restaurant.id == self.restaurant.id

	def is_available_in_any_branch(self):
		return self.available and any(pkg.available for pkg in PackageBranchDetails.objects.filter(package=self))

	def get_avg_rating(self):
		from browse.utils_db import get_rating_package
		return get_rating_package(self.id)

	def get_all_offers(self):
		""":returns list of PackageBranchDetails that has any offer"""
		if not self.available:
			return []
		packs = PackageBranchDetails.objects.filter(package=self, available=True)
		offered_pack = list(filter(lambda p: p.has_any_offer(), packs))
		return offered_pack

	def has_offer_in_any_branch(self):
		return any(map(lambda p: p.has_any_offer(), PackageBranchDetails.objects.filter(package=self)))

	def has_any_buy_get_offer(self):
		return any(map(lambda p: p.has_buy_get_offer(), PackageBranchDetails.objects.filter(package=self)))

	def has_any_discount_offer(self):
		return any(map(lambda p: p.has_discount_offer(), PackageBranchDetails.objects.filter(package=self)))

	def available_branches(self):
		return PackageBranchDetails.objects.filter(package=self, available=True) and self.available


class IngredientList(models.Model):
	"""
	Keeps which cuisine has which ingredients
	"""
	package = models.ForeignKey(Package, on_delete=models.CASCADE)
	ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

	class Meta:
		verbose_name = "IngredientList"
		verbose_name_plural = "IngredientLists"

	def get_absolute_url(self):
		return reverse("IngredientList_detail", kwargs={"pk": self.pk})


class PackageRating(models.Model):
	"""
	Ratings for a cuisine rated by a customer
	"""
	rating = models.IntegerField('Rating', default=5, null=False)
	package = models.ForeignKey(Package, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Package Rating"
		verbose_name_plural = "Package Ratings"
		unique_together = [['package', 'user']]

	def get_absolute_url(self):
		return reverse("browse:PackageRating", kwargs={"id": self.pk})

	def __str__(self):
		return self.package.__str__() + " " + str(self.rating) + " from " + self.user.__str__()


class PackageComment(models.Model):
	"""
	Comments of customers for a cuisine
	"""
	comment = models.CharField('User Comment', max_length=250, blank=False, null=False)
	time = models.DateTimeField(verbose_name="Post Time", auto_now=True, auto_now_add=False)
	package = models.ForeignKey(Package, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='package_comment_author_user')
	reacts = models.ManyToManyField(User, through='PackageCommentReact', related_name='package_react_user')

	class Meta:
		verbose_name = "Package Comment"
		verbose_name_plural = "Package Comments"
		unique_together = [['package', 'user']]

	def get_absolute_url(self):
		return reverse("browse:PackageComment", kwargs={"id": self.pk})


class PackageCommentReact(models.Model):
	"""
	Like, Dislike reacts of customers for others comment on a cuisine
	"""
	post = models.ForeignKey(PackageComment, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	liked = models.BooleanField(verbose_name='Liked', default=False)
	disliked = models.BooleanField(verbose_name='Disliked', default=False)

	class Meta:
		verbose_name = "Package Comment React"
		verbose_name_plural = "Package Comment Reacts"
		unique_together = [['post', 'user']]

	def get_absolute_url(self):
		return reverse("browse:PackageCommentReact", kwargs={"id": self.pk})


class BranchRating(models.Model):
	"""
	Ratings for a Branch rated by a customer
	"""
	rating = models.IntegerField('Rating', default=5, null=False)
	branch = models.ForeignKey('accounts.RestaurantBranch', on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Branch Rating"
		verbose_name_plural = "Branch Ratings"
		unique_together = [['branch', 'user']]

	def get_absolute_url(self):
		return reverse("browse:BranchRating", kwargs={"id": self.pk})


class BranchComment(models.Model):
	"""
	Comments of customers for a branch
	"""
	comment = models.CharField('User Comment', max_length=250, blank=False, null=False)
	time = models.DateTimeField(verbose_name="Post Time", auto_now=True, auto_now_add=False)
	branch = models.ForeignKey('accounts.RestaurantBranch', on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='branch_comment_author_user')
	reacts = models.ManyToManyField(User, through='BranchCommentReact', related_name='branch_react_user')

	class Meta:
		verbose_name = "Branch Comment"
		verbose_name_plural = "Branch Comments"
		unique_together = [['branch', 'user']]

	def get_absolute_url(self):
		return reverse("browse:BranchComment", kwargs={"id": self.pk})


class BranchCommentReact(models.Model):
	"""
	Like, Dislike reacts of customers for others comment on a branch
	"""
	post = models.ForeignKey(BranchComment, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	liked = models.BooleanField(verbose_name='Liked', default=False)
	disliked = models.BooleanField(verbose_name='Disliked', default=False)

	class Meta:
		verbose_name = "Branch Comment React"
		verbose_name_plural = "Branch Comment Reacts"
		unique_together = [['post', 'user']]

	def get_absolute_url(self):
		return reverse("browse:BranchCommentReact", kwargs={"id": self.pk})


# ------------------------- Offers ------------------------------

class PackageBranchDetails(models.Model):
	"""
	Entity of a cuisine's info maintained by any individual branch of a restaurant
	Keeps whether a package is available at a branch and
	Offer details associated with that cuisine in that branch
	"""
	package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='branch_specific_details')
	branch = models.ForeignKey('accounts.RestaurantBranch', on_delete=models.CASCADE)

	available = models.BooleanField(default=True)

	NONE = 'N'
	DISCOUNT = 'D'
	BUY_N_GET_N = 'B'
	OFFER_TYPES = ((NONE, 'None'), (DISCOUNT, 'Discount'), (BUY_N_GET_N, 'Buy N Get N'))

	offer_type = models.CharField(verbose_name="Offer Type", max_length=1, choices=OFFER_TYPES, default=NONE)
	offer_start_date = models.DateField(verbose_name="Offer starting date", null=True)
	offer_expire_date = models.DateField(verbose_name="Offer expiry date", null=True, blank=True)
	offer_discount = models.IntegerField(verbose_name="Discount amount", default=0)
	offer_buy_n = models.IntegerField(verbose_name="Buy N", default=1)
	offer_get_n = models.IntegerField(verbose_name="Get N", default=0)

	class Meta:
		verbose_name = "Package Details of Branch"
		verbose_name_plural = "Packages Details of Branches"
		unique_together = [['package', 'branch']]

	def __str__(self):
		return self.package.pkg_name + ", " + str(self.package.price) + ", " + str(self.available)

	def has_any_offer(self):
		from datetime import date
		return self.is_available() and self.offer_type != self.NONE and self.offer_start_date <= date.today() <= self.offer_expire_date

	def has_discount_offer(self):
		from datetime import date
		return self.is_available() and self.offer_type == self.DISCOUNT and self.offer_start_date <= date.today() <= self.offer_expire_date

	def has_buy_get_offer(self):
		from datetime import date
		return self.is_available() and self.offer_type == self.BUY_N_GET_N and self.offer_start_date <= date.today() <= self.offer_expire_date

	def is_available(self):
		return self.available and self.package.available

	@staticmethod
	def add_package_to_all_branches(restaurant, package):
		branches = RestaurantBranch.objects.filter(restaurant=restaurant)
		for branch in branches:
			PackageBranchDetails.objects.get_or_create(package=package, branch=branch)

	def set_discount_offer(self, start_date, end_date, discount_val):
		self.clear_offer(commit=False)
		self.offer_start_date = start_date
		self.offer_expire_date = end_date
		self.offer_discount = discount_val
		self.offer_type = PackageBranchDetails.DISCOUNT
		self.save()

	def set_buy_get_offer(self, start_date, end_date, buy_n, get_n):
		self.clear_offer(commit=False)
		self.offer_start_date = start_date
		self.offer_expire_date = end_date
		self.offer_buy_n = buy_n
		self.offer_get_n = get_n
		self.offer_type = PackageBranchDetails.BUY_N_GET_N
		self.save()

	def clear_offer(self, commit=True):
		self.offer_type = self.NONE
		self.offer_discount = 0
		self.offer_buy_n = 1
		self.offer_get_n = 0
		if commit:
			self.save()

	def get_absolute_url(self):
		return reverse('manager:package-branch-details', kwargs={"pk": self.pk})

	def get_offer_details(self):
		offer = 'No offers'
		if self.is_available() and self.has_any_offer():
			if self.offer_type == PackageBranchDetails.DISCOUNT:
				offer = str(round(self.offer_discount * 100.0 / self.package.price)) + "% Discount"
			elif self.offer_type == PackageBranchDetails.BUY_N_GET_N:
				offer = "Buy " + str(self.offer_buy_n) + " Get " + str(self.offer_get_n) + " for Free"
		return offer

	def get_buying_price(self, order_quantity=1):
		if self.has_buy_get_offer():
			return self.package.price * order_quantity
		elif self.has_discount_offer():
			return (self.package.price - self.offer_discount) * order_quantity
		else:
			return self.package.price * order_quantity

	def is_deliverable_to(self, coordinates):
		"""
		:param coordinates: (x,y) format
		"""
		print("distance=", self.branch.distance(coordinates))
		return self.is_available() and self.branch.distance(coordinates) < RestaurantBranch.MAX_DELIVERABLE_DISTANCE
