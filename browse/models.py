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

#
# class PackageRating(models.Model):
# 	rating = models.IntegerField('Rating', default=5)
# 	package = models.ForeignKey(Package, on_delete=models.CASCADE)
# 	user = models.ForeignKey(User, on_delete=models.CASCADE)
#
# 	def get_absolute_url(self):
# 		return reverse("browse:PackageRating", kwargs={"id": self.pk})
#
#
# class PackageReview(models.Model):
# 	rating = models.FloatField('')
# 	desc = models.CharField('User Comment', max_length=250)
# 	time = models.DateTimeField(verbose_name="Post Time", auto_now=True, auto_now_add=False)
# 	# likes = models.IntegerField(verbose_name='Number of Likes', default=0)
# 	# dislikes = models.IntegerField(verbose_name='Number of Dislikes', default=0)
# 	package = models.ForeignKey(Package, on_delete=models.CASCADE)
# 	user = models.ForeignKey(User, on_delete=models.CASCADE)
# 	reacts = models.ManyToManyField(User, through='Reacts')
#
# 	# def get_absolute_url(self):
# 	# 	return reverse("browse:PackageReview", kwargs={"id": self.pk})
#
#
# class Reacts(models.Model):
# 	post = models.ForeignKey(PackageReview, on_delete=models.CASCADE)
# 	user = models.ForeignKey(User, on_delete=models.CASCADE)
#
# 	liked = models.BooleanField(verbose_name='Liked', default=False)
# 	disliked = models.BooleanField(verbose_name='Disliked', default=False)
#
# 	class Meta:
# 		verbose_name = "React"
# 		verbose_name_plural = "Reacts"
#
# 	# def get_absolute_url(self):
# 	# 	return reverse("browse:ReactCount", kwargs={"id": self.pk})