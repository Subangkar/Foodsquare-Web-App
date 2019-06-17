from django.db import models
from django.urls import reverse
# from location_field.models.spatial import LocationField
from location_field.models.plain import PlainLocationField
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class Restaurant(models.Model):
	restaurant_id = models.CharField(max_length=50, unique=True, blank=False, null=False)
	restaurant_name = models.CharField(max_length=50, blank=False, null=False)

	class Meta:
		verbose_name = "Restaurant"
		verbose_name_plural = "Restaurants"

	def __str__(self):
		return self.restaurant_name

	def get_absolute_url(self):
		return reverse("Restaurant_detail", kwargs={"id": self.pk})


class ContactInfo(models.Model):
	# phone = models.PhoneNumberField()
	# mobile = models.PhoneNumberField()

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


class Branch(models.Model):
	branch_id = models.CharField(max_length=50, unique=True, null=False, blank=False)
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


class Ingredient(models.Model):
	name = models.CharField(max_length=50)
	category = models.CharField(max_length=50)

	class Meta:
		verbose_name = "Ingredient"
		verbose_name_plural = "Ingredients"

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("Ingredient_detail", kwargs={"pk": self.pk})


class Item(models.Model):
	item_name = models.CharField(max_length=50)

	ingr_list = models.ManyToManyField(Ingredient, through='IngredientList')

	class Meta:
		verbose_name = "Item"
		verbose_name_plural = "Items"

	def __str__(self):
		return self.item_name

	def get_absolute_url(self):
		return reverse("Item_detail", kwargs={"pk": self.pk})


class Package(models.Model):
	pkg_name = models.CharField(max_length=50)
	for_n_persons = models.IntegerField(default=1)
	price = models.IntegerField(blank=False)
	available = models.BooleanField(default=True)
	image = models.ImageField(upload_to='menu/', default='menu/default.png')

	restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

	item_list = models.ManyToManyField(Item, through='ItemList')

	class Meta:
		verbose_name = "Package"
		verbose_name_plural = "Packages"

	def __str__(self):
		return self.pkg_name

	def get_absolute_url(self):
		return reverse("Package_detail", kwargs={"pk": self.pk})


class ItemList(models.Model):
	pkg_id = models.ForeignKey(Package, on_delete=models.CASCADE)
	item_id = models.ForeignKey(Item, on_delete=models.CASCADE)

	class Meta:
		verbose_name = "ItemList"
		verbose_name_plural = "ItemLists"

	# def __str__(self):
	# 	return self.item_name

	def get_absolute_url(self):
		return reverse("ItemList_detail", kwargs={"pk": self.pk})


class IngredientList(models.Model):
	item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
	ingr_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

	class Meta:
		verbose_name = "IngredientList"
		verbose_name_plural = "IngredientLists"

	# def __str__(self):
	# 	return self.name

	def get_absolute_url(self):
		return reverse("IngredientList_detail", kwargs={"pk": self.pk})
