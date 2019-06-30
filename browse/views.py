# Create your views here.
from itertools import chain

from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView
from browse.utils import *
from browse.models import *


def viewRestaurants(request):
	return render(request, "browse/restaurants.html", {})


# for debug purpose only
def viewRaw(request):
	return render(request, "browse/base-banner.html", {})


class Index(TemplateView):
	template_name = 'browse/index.html'

	def get_context_data(self, **kwargs):
		with open("sessionLog.txt", "a") as myfile:
			myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")
		ctx = {'loggedIn': False}
		if self.request.user.is_authenticated:
			ctx['loggedIn'] = True
		ctx['restaurant_list'] = Restaurant.objects.all()

		return ctx


class pkg_t:
	def __init__(self, name='', img='', price='', rating='', url='/', ing_list=None, desc=''):
		if ing_list is None:
			ing_list = []
		self.name = name
		self.img = img
		self.price = "$" + str(price)
		self.rating = range(int(rating))
		self.url = "/browse/item/" + url
		self.ing_list = ing_list
		self.desc = desc


class Order(TemplateView):
	template_name = 'browse/order.html'

	def get_context_data(self, **kwargs):
		with open("sessionLog.txt", "a") as myfile:
			myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")
		# item = pkg_t('toys(barbie)', 'browse/images/cuisine2.jpg', '$575.00', '5', '/browse/item/')
		pkg_list = [pkg_t(name=pkgobj.pkg_name, img=pkgobj.image, price=pkgobj.price, rating='5', url=str(pkgobj.id))
		            for pkgobj in Package.objects.all()]

		ctx = {'loggedIn': False, 'item_list': pkg_list }
		if self.request.user.is_authenticated:
			ctx['loggedIn'] = True
		return ctx


class SearchMenu(TemplateView):
	template_name = 'browse/order.html'

	def get_context_data(self, **kwargs):
		with open("sessionLog.txt", "a") as myfile:
			myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")
		query = self.request.GET.get('menu_search')
		price_range = self.request.GET.get('range')
		pkg_list = []
		if query is not None:
			queryset2 = [ingobj.pack_id for ingobj in IngredientList.objects.filter(ingr_id__name__icontains=query)]
			# ing_list = [ingobj.id for ingobj in Ingredient.objects.filter(name__icontains = query)]
			# queryset2 = IngredientList.objects.filter(ingr_id__in = ing_list)
			print(queryset2)
			# queryset2 = Package.objects.raw(" Select * from browse_package where ")
			queryset1 = Package.objects.filter(
				Q(pkg_name__icontains=query)
			)
			# # print(queryset2)
			# print(list(queryset1))
			result_list = list(dict.fromkeys(list(queryset1) + queryset2))
			result_list.sort(key=lambda x: x.pkg_name, reverse=False)
			# result_list = sorted(
			# 	chain(list(queryset1) , queryset2),
			# 	key=lambda instance: instance.pkg_name)
			pkg_list = [pkg_t(name=pkgobj.pkg_name, img=pkgobj.image, price=pkgobj.price, rating='5', url=str(pkgobj.id))
						for pkgobj in result_list]

		else:
			print(price_range)

		ctx = {'loggedIn': False, 'item_list': pkg_list }
		if self.request.user.is_authenticated:
			ctx['loggedIn'] = True
		return ctx




class PackageDetails(TemplateView):
	template_name = 'browse/item.html'

	def get(self, request, *args, **kwargs):
		if kwargs.get('id') is None or not isinstance(kwargs['id'], int):
			return redirect('/order/')
		return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		with open("sessionLog.txt", "a") as myfile:
			myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")
		id = kwargs['id']
		pkg = Package.objects.get(id=id)
		ing_list = [ingobj.ingr_id.name for ingobj in IngredientList.objects.filter(pack_id=id)]
		pkg = pkg_t(name=pkg.pkg_name, price=pkg.price, img=pkg.image, rating='5', ing_list=ing_list,
		            desc=pkg.details,
		            url=str(pkg.id))
		# ing_list = list(IngredientList.objects.all().filter(pack_id=id).values('ingr_id'))
		# print(pkg.get_absolute_url())
		ctx = {'loggedIn': False, 'item': pkg, 'item_img': [pkg.img]}
		if self.request.user.is_authenticated:
			ctx['loggedIn'] = True
		return ctx


class RestaurantList(ListView):
	template_name = 'browse/restaurants.html'
	queryset = Restaurant.objects.all()
	context_object_name = 'restaurants'
	# print(queryset)