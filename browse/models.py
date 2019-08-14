from django.db import models
from django.urls import reverse

# Create your models here.
from accounts.models import Restaurant, User, RestaurantBranch


# from browse.views import PackageDetails


class Ingredient(models.Model):
	name = models.CharField(max_length=50)

	class Meta:
		verbose_name = "Ingredient"
		verbose_name_plural = "Ingredients"

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("Ingredient_detail", kwargs={"pk": self.pk})


class Package(models.Model):
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


class IngredientList(models.Model):
	pack_id = models.ForeignKey(Package, on_delete=models.CASCADE)
	ingr_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

	class Meta:
		verbose_name = "IngredientList"
		verbose_name_plural = "IngredientLists"

	def get_absolute_url(self):
		return reverse("IngredientList_detail", kwargs={"pk": self.pk})


class PackageRating(models.Model):
	rating = models.IntegerField('Rating', null=False)
	package = models.ForeignKey(Package, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Package Rating"
		verbose_name_plural = "Package Ratings"
		unique_together = [['package', 'user']]

	def get_absolute_url(self):
		return reverse("browse:PackageRating", kwargs={"id": self.pk})


class PackageComment(models.Model):
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
	rating = models.IntegerField('Rating', null=False)
	branch = models.ForeignKey('accounts.RestaurantBranch', on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Branch Rating"
		verbose_name_plural = "Branch Ratings"
		unique_together = [['branch', 'user']]

	def get_absolute_url(self):
		return reverse("browse:BranchRating", kwargs={"id": self.pk})


class BranchComment(models.Model):
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
	Package Details Info for a Branch
	Keeps whether a package is available at a branch and
	Offer details associated with that package in that branch

		available: true if this branch has the package currently
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

	def has_any_offer(self):
		from datetime import date
		return self.offer_type != self.NONE and self.offer_start_date <= date.today() <= self.offer_expire_date

	@staticmethod
	def add_package_to_all_branches(restaurant, package):
		branches = RestaurantBranch.objects.filter(restaurant=restaurant)
		for branch in branches:
			PackageBranchDetails.objects.get_or_create(package=package, branch=branch)


class UserOffer(models.Model):
	"""
	Keeps offers from branch manger to specific user
	Generates a code for a user which will be used to avail the offer

		used(Boolean): refers whether this offer has been used by user for at least once

		offer_count(int): refers to how many times this offer can be availed

		offer_code(str): unique code to submit during order to avail the offer
	"""

	def uniqueKey(self, N=5):
		import random
		import string
		while True:
			code = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=N))
			if not UserOffer.objects.filter(offer_code=code).exists():
				return code

	user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='branch_specific_offer')
	branch = models.ForeignKey('accounts.RestaurantBranch', on_delete=models.CASCADE)

	used = models.BooleanField(default=False)
	offer_start_date = models.DateField(verbose_name="Offer starting date", auto_now_add=True)
	offer_expire_date = models.DateField(verbose_name="Offer expiry date", null=True, blank=True)
	offer_discount = models.IntegerField(verbose_name="Discount amount", default=0)
	offer_count = models.IntegerField(default=1)
	offer_code = models.CharField(max_length=5, default=uniqueKey)

	class Meta:
		verbose_name = "User Offer Details of Branch"
		verbose_name_plural = "Users Offer Details of Branches"

	def is_available_now(self):
		from datetime import date
		return self.offer_count and self.offer_start_date <= date.today() <= self.offer_expire_date
