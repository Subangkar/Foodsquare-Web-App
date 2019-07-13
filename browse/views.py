# Create your views here.
import json

from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from accounts.models import *  # Delivery, Order
from browse.models import *
from browse.utils import *


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


class Order(TemplateView):
	template_name = 'browse/order.html'

	def get_context_data(self, **kwargs):
		with open("sessionLog.txt", "a") as myfile:
			myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")
		entry_name = self.request.GET.get('menu_search')
		price_range = self.request.GET.get('range')
		pkg_list = Package.objects.all()
		if entry_name is not None:
			minprice = (float(str(price_range).split('-')[0].strip()[1:]))
			maxprice = (float(str(price_range).split('-')[1].strip()[1:]))
			queryset2 = [ingobj.pack_id for ingobj in
			             IngredientList.objects.filter(ingr_id__name__icontains=entry_name)]
			# queryset2 = Package.objects.raw(" Select * from browse_package where ")
			queryset1 = Package.objects.filter(
				Q(pkg_name__icontains=entry_name) & Q(price__range=(minprice, maxprice))
			)
			result_list = list(dict.fromkeys(list(queryset1) + queryset2))
			result_list.sort(key=lambda x: x.pkg_name, reverse=False)
			filtered_result = []
			for x in result_list:
				if minprice <= x.price <= maxprice:
					filtered_result.append(x)
			pkg_list = filtered_result
		ctx = {'loggedIn': False, 'item_list': pkg_list, 'rating': range(5)}
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
		# print(IngredientList.objects.select_related('ingr_id').filter(id))
		ing_list = [ingobj.ingr_id.name for ingobj in IngredientList.objects.filter(pack_id=pkg.id)]
		# # ing_list = list(IngredientList.objects.all().filter(pack_id=id).values('ingr_id'))
		ctx = {'loggedIn': False, 'item': pkg, 'item_img': [pkg.image], 'ing_list': ing_list, 'rating': range(5)}
		if self.request.user.is_authenticated:
			ctx['loggedIn'] = True
		return ctx


class OrderElement_t:
	def __init__(self, id=1):
		self.quantity = 1
		self.pkg = Package.objects.get(id=id)


class CheckoutView(TemplateView):
	template_name = 'browse/checkout.html'

	def get(self, request, *args, **kwargs):
		if not self.request.user.is_authenticated:
			return redirect(reverse('accounts:login'))
		else:
			return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		elements = [OrderElement_t(1), OrderElement_t(2)]
		ctx = {'num_items': range(0, len(elements)), 'elements': elements}
		return ctx

	def post(self, request, *args, **kwargs):
		print(pretty_request(request))

		if not (self.request.user.is_authenticated and self.request.user.is_customer):
			return

		pkg_list = json.loads(request.POST.get('item-list'))['pkg-list']
		houseNo = request.POST.get('house-no')
		roadNo = request.POST.get('road-no')
		blockNo = request.POST.get('block-no')
		apartmentNo = request.POST.get('apartment-no')
		area = request.POST.get('area')
		mobileNo = request.POST.get('mobile-no')

		# b'csrfmiddlewaretoken=YG4XDr7l46ARcQ9kdLBNDzQmQ5OVwikfRypkoV8r4tJIYjAIeinEpBt0F3ECRBez&item-list=%7B%22pkg-list%22%3A%5B%7B%22id%22%3A1%2C%22quantity%22%3A4%2C%22price%22%3A150%7D%2C%7B%22id%22%3A5%2C%22quantity%22%3A5%2C%22price%22%3A220%7D%2C%7B%22id%22%3A4%2C%22quantity%22%3A1%2C%22price%22%3A250%7D%5D%7D&
		# house-no=&road-no=&block-no=&apartment-no=&area=&mobile-no='

		delivery = Delivery(address=area,
		                    address_desc=apartmentNo + ', ' + houseNo + ', ' + roadNo + ', ' + blockNo).save()
		order = Order(user=self.request.user, mobileNo=mobileNo, delivery=delivery).save()

		for pkg in pkg_list:
			OrderPackageList(order=order, package=Package.objects.get(id=pkg.id)).save()

		# return JsonResponse(json.loads(request.POST.get('item-list')))
		return HttpResponse('<head><meta http-equiv="refresh" content="5;url=/" /></head>' +
		                    '<body><h1> Your Order has been successfullt placed in queue</h1>\n\nRedirecting...</body')


# return HttpResponse((request.POST.get('item-list')))


class RestaurantList(TemplateView):
	template_name = 'browse/restaurants.html'

	def get_context_data(self, **kwargs):
		with open("sessionLog.txt", "a") as myfile:
			myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")
		# item = pkg_t('toys(barbie)', 'browse/images/cuisine2.jpg', '$575.00', '5', '/browse/item/')
		entry_name = self.request.GET.get('menu_search')
		price_range = self.request.GET.get('range')
		rest_list = list(Restaurant.objects.exclude(restaurant_key='0'))

		ctx = {'loggedIn': False, 'restaurants': rest_list}
		if self.request.user.is_authenticated:
			ctx['loggedIn'] = True
		return ctx


class RestaurantDetails(TemplateView):
	template_name = 'browse/restaurant_home.html'

	def get_context_data(self, **kwargs):
		with open("sessionLog.txt", "a") as myfile:
			myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")
		# item = pkg_t('toys(barbie)', 'browse/images/cuisine2.jpg', '$575.00', '5', '/browse/item/')
		# entry_name = self.request.GET.get('menu_search')
		# price_range = self.request.GET.get('range')
		rest = Restaurant.objects.get(id=kwargs['id'])

		pkg_list = list(Package.objects.filter(restaurant=rest))
		print(pkg_list)
		ctx = {'loggedIn': False, 'item_list': pkg_list, 'restaurant': rest}
		if self.request.user.is_authenticated:
			ctx['loggedIn'] = True
		return ctx
