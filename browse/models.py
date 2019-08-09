from django.db import models
from django.urls import reverse

# Create your models here.
from accounts.models import Restaurant, User


# from browse.views import PackageDetails


class Ingredient(models.Model):
	name = models.CharField(max_length=50)

	# category = models.CharField(max_length=50)

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

	class Meta:
		verbose_name = "Package"
		verbose_name_plural = "Packages"

	def __str__(self):
		return self.pkg_name

	def get_absolute_url(self):
		return reverse("browse:package-details", kwargs={"id": self.pk})


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
