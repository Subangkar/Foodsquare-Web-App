import functools
import json

import requests
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
		pkg_list = Package.objects.all()
		rest_list = Restaurant.objects.all()
		ctx = {'loggedIn': self.request.user.is_authenticated, 'restaurant_list': Restaurant.objects.all(),
		       'item_list': pkg_list[:3], 'restaurants': rest_list[0:4]}
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
			queryset2 = [ingobj.package for ingobj in
			             IngredientList.objects.filter(ingredient__name__icontains=entry_name)]
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
		ing_list = [ingobj.ingredient.name for ingobj in IngredientList.objects.filter(package=pkg)]

		user_id = self.request.user.id if self.request.user.is_authenticated else 0
		comments = get_reviews_package(user_id, id)
		user_rating = None
		if self.request.user.is_authenticated and PackageRating.objects.filter(user=self.request.user,
		                                                                       package=pkg).exists():
			user_rating = PackageRating.objects.get(user=self.request.user, package=pkg)
		print(get_rating_count_package(id))
		ctx = {'loggedIn': self.request.user.is_authenticated, 'item': pkg, 'item_img': [pkg.image],
		       'ing_list': ing_list, 'comments': comments, 'ratings': get_rating_count_package(id),
		       'avg_rating': get_rating_package(id)
			, 'user_rating': user_rating}
		return ctx


class CheckoutView(TemplateView):
	template_name = 'browse/checkout.html'

	def get(self, request, *args, **kwargs):
		if not self.request.user.is_authenticated:
			return redirect(reverse('accounts:login'))
		else:
			return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		elements = []
		ctx = {'num_items': range(0, len(elements)), 'elements': elements,
		       'loggedIn': self.request.user.is_authenticated}
		return ctx

	def post(self, request, *args, **kwargs):
		"""PackageID is id of PackageBranchDetails"""
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

		branch = RestaurantBranch.objects.get(id=branchID)
		delivery = Delivery.objects.create(address=area,
		                                   address_desc=apartmentNo + ', ' + houseNo + ', ' + roadNo + ', ' + blockNo)

		total_price = 0
		for pkg in pkg_list:
			total_price += pkg['price']
		from webAdmin import utils
		total_price += utils.get_delivery_charge(total_price)

		# set payment_type + status
		payment = None
		if request.POST.get('bkash_payment') is not None:
			print('success')
			payment = Payment.objects.create(price=total_price, payment_type=Payment.ONLINE,
			                                 bkash_ref=request.POST.get('ref_no'), payment_status=Payment.DUE)
		else:
			print('cash')
			payment = Payment.objects.create(price=total_price, payment_type=Payment.CASH, payment_status=Payment.DUE)

		order = Order.objects.create(user=self.request.user, mobileNo=mobileNo, delivery=delivery, branch=branch,
		                             payment=payment)

		for pkg in pkg_list:
			# print(Package.objects.get(id=pkg['id']))
			package = PackageBranchDetails.objects.get(id=pkg['id']).package
			OrderPackageList.objects.create(order=order, package=package, quantity=int(pkg['quantity']),
			                                price=pkg['price'])
		from customer.utils_db import send_notification
		send_notification(order.user.id, "Your order: " + str(
			order.id) + " from " + order.branch.branch_name + " with " + str(
			len(pkg_list)) + " items has been placed in manager's queue for confirmation.")

		return redirect("/")


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

	def __eq__(self, other):
		return self.branch == other.branch if self.branch else self.id == other.id

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
		if branches[0].distance(coord) < RestaurantBranch.MAX_DELIVERABLE_DISTANCE:
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

		qset = RestaurantBranch.objects.filter(
			Q(branch_name__icontains=query) | Q(restaurant__restaurant_name__icontains=query) | Q(
				restaurant__package__category__icontains=query)).distinct()
		if show == 'all':
			rest_list = frozenset(x.restaurant for x in qset)
			rest_list = [RestBranch(x) for x in rest_list]
		else:
			rest_list = branchesInRadius(coord=coord, queryset=qset)
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
		user_id = self.request.user.id if self.request.user.is_authenticated else 0
		comments = get_reviews_branch(user_id, kwargs['id'])

		# print(pkg_list)
		ctx = {'loggedIn': self.request.user.is_authenticated, 'item_list': pkg_list, 'categories': categories,
		       'restaurant': RestBranch(restaurant=branch.restaurant, branch=branch),
		       'rating': get_rating_branch(kwargs['id']),
		       'comments': comments}
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

		# pkg_list = [p.package for p in get_available_packages_restaurant(rest_id=rest.id)]
		pkg_list = Package.objects.filter(restaurant__id=rest.id)

		categories = set([item.category for item in pkg_list])
		# print(pkg_list)
		branch_list = RestaurantBranch.objects.filter(restaurant__id=kwargs['id'])

		ctx = {'loggedIn': self.request.user.is_authenticated, 'item_list': pkg_list, 'categories': categories,
		       'restaurant': RestBranch(restaurant=rest, branch=None), 'rating': get_rating_restaurant(kwargs['id']),
		       'branch_list': branch_list}
		return ctx


#
def reactSubmit(request, id):
	print(request)
	if not request.user.is_authenticated:
		return
	pkg_id = request.POST.get('pkg-id')
	branch_id = request.POST.get('branch-id')
	react = request.POST.get('react')
	post_id = request.POST.get('comment-id')
	nlike, ndislike = 0, 0
	user = request.user
	if pkg_id is not None:
		nlike, ndislike = post_comment_react_package(user, post_id, react)

	elif branch_id is not None:
		nlike, ndislike = post_comment_react_branch(user, post_id, react)
	print(pkg_id, " ", nlike, " ", ndislike)
	return JsonResponse({'nlikes': nlike, 'ndislikes': ndislike})


def submitReview(request, id):
	pkg_id = request.POST.get('pkg-id')
	branch_id = request.POST.get('branch-id')
	comment = request.POST.get('comment')
	user = request.user
	# print(pkg_id, " ", comment, " ", user)
	print(branch_id, " ", comment, " ", user)

	# package = Package.objects.exclude(user=request.user).get(id=pkg_id)
	if pkg_id is not None:
		post_comment_package(user, pkg_id, comment)
	elif branch_id is not None:
		post_comment_branch(user, branch_id, comment)
	return JsonResponse({'success': 'success'})


def submitPackageRating(request, id):
	pkg_id = request.POST.get('pkg-id')
	rating = request.POST.get('rating')
	user = request.user
	print(pkg_id, " ", rating, " ", user)

	# package = Package.objects.exclude(user=request.user).get(id=pkg_id)
	post_rating_package(user, pkg_id, rating)
	return JsonResponse({'success': True})


def submitBranchRating(request, id):
	branch_id = request.POST.get('restaurant-id')
	rating = request.POST.get('rating')
	user = request.user

	post_rating_branch(user, branch_id, rating)
	return JsonResponse({'success': True})


def FilteredProducts(request):
	entry_name = request.GET.get('menu_name')
	price_range_min = request.GET.get('min_range')
	price_range_max = request.GET.get('max_range')
	rating = request.GET.get('rating')
	category = ""
	if not entry_name:
		entry_name = ''
	if not price_range_min:
		price_range_min = "0"
	if not price_range_max:
		price_range_max = "10000"
	pkg_list = get_named_package(entry_name)
	if rating and int(rating) != 0:
		pkg_list &= get_rated_package(int(rating))
	pkg_list &= get_price_range_package(float(price_range_min), float(price_range_max))
	if category != '':
		pkg_list &= get_category_packages(category)
	print(pkg_list)

	return render(request, 'browse/product_list.html', {'item_list': pkg_list})


def branch_pkg_availability(request):
	id = request.GET.get('id')
	coord = request.GET.get('coord')
	if coord:
		return render(request, 'browse/branch_availability.html', {'branchList': get_deliverable_offers(id, coord)})

	return JsonResponse({'success': False})


def aboutSection(request):
	return render(request, 'browse/about.html')
