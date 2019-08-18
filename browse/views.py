# Create your views here.
import functools
import json

from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from accounts.models import *  # Delivery, Order
from browse.models import *
from browse.utils import *

from accounts.models import Payment
from browse.utils_db import *


def getUniqueBkashRef(N=10):
	while True:
		key = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=N))
		if not Payment.objects.filter(bkash_ref=key).exists():
			return key


def viewRestaurants(request):
	return render(request, "browse/restaurants.html", {})


# for debug purpose only
def viewRaw(request):
	return render(request, "browse/base-banner.html", {})


def bkashPayment(request):
	return JsonResponse({'ref': getUniqueBkashRef()})


class Index(TemplateView):
	template_name = 'browse/index.html'

	def get_context_data(self, **kwargs):
		with open("sessionLog.txt", "a") as myfile:
			myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")
		ctx = {'loggedIn': self.request.user.is_authenticated, 'restaurant_list': Restaurant.objects.all()}
		return ctx


class OrderView(TemplateView):
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
		# comments = PackageReview.objects.filter(package=pkg)
		user_id = self.request.user.id if self.request.user.is_authenticated else 0
		comments = get_reviews_package(user_id, id)
		print(get_rating_count_package(id))
		ctx = {'loggedIn': self.request.user.is_authenticated, 'item': pkg, 'item_img': [pkg.image],
		       'ing_list': ing_list, 'comments': comments, 'ratings': get_rating_count_package(id),
		       'avg_rating': get_rating_package(id)}
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
		                    address_desc=apartmentNo + ', ' + houseNo + ', ' + roadNo + ', ' + blockNo)

		total_price = 0
		for pkg in pkg_list:
			total_price += pkg['price'] * pkg['quantity']
		total_price += total_price * 0.1  # 10% delivery charge

		# set payment_type + status
		payment = None
		if request.POST.get('bkash_payment') is not None:
			print('success')

			# random price are inserted
			payment = Payment(price=total_price, payment_type=Payment.ONLINE,
			                  bkash_ref=request.POST.get('ref_no'), payment_status=Payment.DUE)
		elif request.POST.get('COD_payment') is not None:
			print('failure')
			payment = Payment(price=total_price, payment_type=Payment.CASH, payment_status=Payment.DUE)
		else:
			print('cash')
			payment = Payment(price=total_price, payment_type=Payment.CASH, payment_status=Payment.DUE)
		# print(payment)
		payment.save()
		delivery.save()
		order = Order(user=self.request.user, mobileNo=mobileNo, delivery=delivery, branch=branch, payment=payment)
		order.save()
		# return JsonResponse(json.loads(request.POST.get('item-list')))
		# print(order)
		for pkg in pkg_list:
			print(Package.objects.get(id=pkg['id']))
			OrderPackageList(order=order, package=Package.objects.get(id=pkg['id']),
			                 quantity=int(pkg['quantity'])).save()

		return redirect("/")


# return redirect(reverse('browse:package-list'))


class RestBranch:
	branch = None
	is_branch = False
	user = None
	restaurant_name = None
	restaurant_key = None
	trade_license = None
	restaurantImg = None
	id = None

	def __init__(self, restaurant, branch=None):
		self.user = restaurant.user
		self.restaurant_name = restaurant.restaurant_name
		self.restaurant_key = restaurant.restaurant_key
		self.trade_license = restaurant.trade_license
		self.restaurantImg = restaurant.restaurantImg
		self.id = restaurant.id
		self.pk = restaurant.pk
		self.get_absolute_url = restaurant.get_absolute_url()

		if branch is not None:
			self.is_branch = True
			self.is_open_now = branch.is_open_now()
			# print(branch.get_absolute_url())
			self.get_absolute_url = branch.get_absolute_url()

		self.addBranch(branch=branch)

	def addBranch(self, branch):
		self.branch = branch
		self.is_branch = self.branch is not None


def branchesInRadius(coord, queryset):
	rest_map = {}
	rest_list = []
	for r in queryset:
		if r.restaurant.id in rest_map:
			rest_map[r.restaurant.id].append(r)
		else:
			rest_map[r.restaurant.id] = [r]
	for rest in rest_map.values():
		branches = sorted(rest, key=functools.cmp_to_key(lambda x, y: x.distance(coord) - y.distance(coord)))
		# print(branches[0].branch_name + ' ' + str(branches[0].distance(coord)))
		if branches[0].distance(coord) < 4:
			def_branch = branches[0]
			for branch in branches:
				if branch.is_open_now():
					def_branch = branch
					break
			rest_list.append(RestBranch(def_branch.restaurant, branch=def_branch))
	# else:
	# 	rest_list.append(RestBranch(branches[0].restaurant, branch=None))
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
		print(pretty_request(self.request))
		with open("sessionLog.txt", "a") as myfile:
			myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")
		query = self.request.GET.get('searchBy_dish_food')
		coord = self.request.GET.get('delivery_area_srch')
		show = self.request.GET.get('show')

		if query is None:
			query = ''

		if coord is None or not coord:
			show = 'all'
		elif coord is not None and show is None:
			show = 'near_me'
			print(' @ ' + coord)

		query_sql = \
			'select distinct accounts_restaurantbranch.*\
			from accounts_restaurantbranch\
					join accounts_restaurant on accounts_restaurantbranch.restaurant_id = accounts_restaurant.id\
					join browse_package on accounts_restaurant.id = browse_package.restaurant_id\
			        join browse_ingredientlist on browse_package.id = browse_ingredientlist.pack_id_id\
					join browse_ingredient on browse_ingredientlist.ingr_id_id = browse_ingredient.id\
			where lower(browse_ingredient.name) like \'%%\' || lower(\'' + query + '\') || \'%%\'\
				or lower(browse_package.pkg_name) like \'%%\' || lower(\'' + query + '\') || \'%%\'\
				or lower(accounts_restaurant.restaurant_name) like \'%%\' || lower(\'' + query + '\') || \'%%\'\
				or lower(accounts_restaurantbranch.branch_name) like \'%%\' || lower(\'' + query + '\') || \'%%\''

		if show == 'all':
			rest_list = list([RestBranch(x.restaurant) for x in RestaurantBranch.objects.raw(query_sql)])
		else:
			rest_list = branchesInRadius(coord=coord, queryset=RestaurantBranch.objects.raw(query_sql))
		print(rest_list)

		ctx = {'loggedIn': self.request.user.is_authenticated, 'restaurants': rest_list,
		       'show_all': (show == 'all'), 'query': query}
		return ctx


class RestaurantBranchDetails(TemplateView):
	template_name = 'browse/restaurant_home.html'

	def get_context_data(self, **kwargs):
		with open("sessionLog.txt", "a") as myfile:
			myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")
		branch = RestaurantBranch.objects.get(id=kwargs['id'])
		# pkg_list = list(Package.objects.filter(restaurant=branch.restaurant))
		pkg_list = list(get_available_packages_branch(branch_id=branch.id))
		categories = set([item.package.category for item in pkg_list])

		# print(pkg_list)
		ctx = {'loggedIn': self.request.user.is_authenticated, 'item_list': pkg_list, 'categories': categories,
		       'restaurant': RestBranch(restaurant=branch.restaurant, branch=branch),
		       'rating': get_rating_branch(kwargs['id'])}
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
		pkg_list = list(get_available_packages_restaurant(rest_id=rest.id))
		categories = set([item.package.category for item in pkg_list])
		# print(pkg_list)
		ctx = {'loggedIn': self.request.user.is_authenticated, 'item_list': pkg_list, 'categories': categories,
		       'restaurant': RestBranch(restaurant=rest, branch=None), 'rating': get_rating_restaurant(kwargs['id'])}
		return ctx


#
def reactSubmit(request, id):
	print(request)
	if not request.user.is_authenticated:
		return
	pkg_id = request.POST.get('pkg-id')
	react = request.POST.get('react')
	post_id = request.POST.get('comment-id')
	# package = Package.objects.exclude(user=request.user).get(id=pkg_id)
	user = request.user
	post_comment_react_package(user, post_id, react)
	return JsonResponse({'nlikes': 5, 'ndislikes': 2})


def submitReview(request, id):
	print(request)
	pkg_id = request.POST.get('pkg-id')
	comment = request.POST.get('comment')
	user = request.user

	# package = Package.objects.exclude(user=request.user).get(id=pkg_id)
	post_comment_package(user, pkg_id, comment)
	return JsonResponse({'success': 'success'})


def submitPackageRating(request, id):
	pkg_id = request.POST.get('pkg-id')
	rating = request.POST.get('rating')
	user = request.user

	# package = Package.objects.exclude(user=request.user).get(id=pkg_id)
	post_rating_package(user, pkg_id, rating)
	return


def reactOn(request, id):
	print(request)
	pkg_id = request.POST.get('pkg-id')
	rating = request.POST.get('rating')
	user = request.user

	# package = Package.objects.exclude(user=request.user).get(id=pkg_id)
	post_rating_package(user, pkg_id, rating)
	return


def submitBranchRating(request):
	branch_id = request.POST.get('restaurant-id')
	rating = request.POST.get('rating')
	user = request.user

	post_rating_branch(user, branch_id, rating)
	return


def FilteredProducts(request):
	entry_name = request.GET.get('menu_search')
	price_range = request.GET.get('range')
	pkg_list = get_named_package(entry_name)
	pkg_list &= get_rated_package(5)
	pkg_list &= get_price_range_package(0, 300)

	return render(request, 'browse/product_list.html', {'item_list': pkg_list})


for pkg in Package.objects.all():
	PackageBranchDetails.add_package_to_all_branches(pkg.restaurant, pkg)
