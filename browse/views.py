# Create your views here.
import functools
import json

from django.db.models import Q
from django.http import HttpResponse
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
		ctx = {'loggedIn': self.request.user.is_authenticated, 'restaurant_list': Restaurant.objects.all()}
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
		ctx = {'loggedIn': self.request.user.is_authenticated, 'item_list': pkg_list, 'rating': range(5)}
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
		ing_list = [ingobj.ingr_id.name for ingobj in IngredientList.objects.filter(pack_id=pkg.id)]
		ctx = {'loggedIn': self.request.user.is_authenticated, 'item': pkg, 'item_img': [pkg.image],
		       'ing_list': ing_list, 'rating': range(5)}
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
		ctx = {'num_items': range(0, len(elements)), 'elements': elements,
		       'loggedIn': self.request.user.is_authenticated}
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
		branchID = request.POST.get('branch-id')

		# b'csrfmiddlewaretoken=YG4XDr7l46ARcQ9kdLBNDzQmQ5OVwikfRypkoV8r4tJIYjAIeinEpBt0F3ECRBez&item-list=%7B%22pkg-list%22%3A%5B%7B%22id%22%3A1%2C%22quantity%22%3A4%2C%22price%22%3A150%7D%2C%7B%22id%22%3A5%2C%22quantity%22%3A5%2C%22price%22%3A220%7D%2C%7B%22id%22%3A4%2C%22quantity%22%3A1%2C%22price%22%3A250%7D%5D%7D&
		# house-no=&road-no=&block-no=&apartment-no=&area=&mobile-no='

		branch = RestaurantBranch.objects.get(id=branchID)
		delivery = Delivery(address=area,
		                    address_desc=apartmentNo + ', ' + houseNo + ', ' + roadNo + ', ' + blockNo).save()
		order = Order(user=self.request.user, mobileNo=mobileNo, delivery=delivery, branch=branch).save()

		for pkg in pkg_list:
			OrderPackageList(order=order, package=Package.objects.get(id=pkg.id)).save()

		# return JsonResponse(json.loads(request.POST.get('item-list')))
		return HttpResponse('<head><meta http-equiv="refresh" content="5;url=/" /></head>' +
		                    '<body><h1> Your Order has been successfullt placed in queue</h1><br><br>Redirecting...</body')


class RestBranch(Restaurant):
	branch = None
	is_branch = False

	def addBranch(self, branch):
		self.branch = branch
		self.is_branch = self.branch is not None


def branchesInRadius(coord):
	rest_map = {}
	rest_list = []
	for r in RestaurantBranch.objects.all():
		if r.restaurant.id in rest_map:
			rest_map[r.restaurant.id].append(r)
		else:
			rest_map[r.restaurant.id] = [r]

	for rest in rest_map.values():
		branches = sorted(rest, key=functools.cmp_to_key(lambda x, y: x.distance(coord) - y.distance(coord)))
		if branches[0].distance(coord) > 4:
			rest_list.append(RestBranch(branches[0].restaurant).addBranch(branch=None))
		else:
			rest_list.append(RestBranch(branches[0].restaurant).addBranch(branch=branches[0]))
	return rest_list


class RestaurantList(TemplateView):
	"""[Renders list of branches in 4km radius]
	Description:
		If no such branch is in radius then None
		Assuming, a restaurant with null key cannot have any branch
	Returns:
		[type] -- [description]
	"""
	template_name = 'browse/restaurants.html'

	def get_context_data(self, **kwargs):
		with open("sessionLog.txt", "a") as myfile:
			myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")
		query = self.request.GET.get('searchBy_dish_food')
		coord = self.request.GET.get('delivery_area_srch')

		show = self.request.GET.get('show')
		rest_list = []
		print(pretty_request(self.request))
		if query is None:
			rest_list = list(Restaurant.objects.exclude(restaurant_key='0'))
		else:
			if show == 'all':
				rest_list = list(RestBranch(x) for x in
				                 Restaurant.objects.exclude(restaurant_key='0').filter(
					                 restaurant_name__icontains=query))
			else:
				rest_list = branchesInRadius(coord=coord)

		ctx = {'loggedIn': self.request.user.is_authenticated, 'restaurants': rest_list}
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
		ctx = {'loggedIn': self.request.user.is_authenticated, 'item_list': pkg_list, 'restaurant': rest}
		return ctx
