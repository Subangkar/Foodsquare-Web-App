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
	def __init__(self, name='', img='', price='', rating='', url='/', ing_list=None, desc='', rest_name=''):
		if ing_list is None:
			ing_list = []
		self.name = name
		self.img = img
		self.price = "BDT." + str(price)
		self.rating = range(int(rating))
		self.url = "/browse/item/" + url
		self.ing_list = ing_list
		self.desc = desc
		self.rest_name = rest_name


class Order(TemplateView):
	template_name = 'browse/order.html'

	def get_context_data(self, **kwargs):
		with open("sessionLog.txt", "a") as myfile:
			myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")
		# item = pkg_t('toys(barbie)', 'browse/images/cuisine2.jpg', '$575.00', '5', '/browse/item/')
		entry_name = self.request.GET.get('menu_search')
		price_range = self.request.GET.get('range')
		pkg_list = [
			pkg_t(name=pkgobj.pkg_name, img=pkgobj.image, price=pkgobj.price, rating='5', url=str(pkgobj.id))
			for pkgobj in Package.objects.all()]
		if entry_name is not None:
			print(entry_name)
			print(str(price_range))
			minprice = (float(str(price_range).split('-')[0].strip()[1:]))
			maxprice = (float(str(price_range).split('-')[1].strip()[1:]))
			# print(str(price_range).split('-')[0].strip()[1:], end='<<\n')
			# print(str(price_range).split('-')[1].strip()[1:], end='<<\n')
			print(minprice)
			print(maxprice)
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
				# print(x.restaurant.restaurant_name)
			pkg_list = [
				pkg_t(name=pkgobj.pkg_name, img=pkgobj.image, price=pkgobj.price, rating='5', url=str(pkgobj.id),
				      rest_name=pkgobj.restaurant.restaurant_name)
				for pkgobj in filtered_result]
		# print(pkg_list[0].rest_name)
		ctx = {'loggedIn': False, 'item_list': pkg_list}
		if self.request.user.is_authenticated:
			ctx['loggedIn'] = True
		return ctx


# class SearchMenu(TemplateView):
# 	template_name = 'browse/order.html'
#
# 	def get_context_data(self, **kwargs):
# 		with open("sessionLog.txt", "a") as myfile:
# 			myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")
# 		query = self.request.GET.get('menu_search')
# 		price_range = self.request.GET.get('range')
# 		pkg_list = []
# 		if query is not None:
# 			queryset2 = [ingobj.pack_id for ingobj in IngredientList.objects.filter(ingr_id__name__icontains=query)]
# 			# queryset2 = Package.objects.raw(" Select * from browse_package where ")
# 			queryset1 = Package.objects.filter(
# 				Q(pkg_name__icontains=query)
# 			)
# 			result_list = list(dict.fromkeys(list(queryset1) + queryset2))
# 			result_list.sort(key=lambda x: x.pkg_name, reverse=False)
# 			pkg_list = [
# 				pkg_t(name=pkgobj.pkg_name, img=pkgobj.image, price=pkgobj.price, rating='5', url=str(pkgobj.id))
# 				for pkgobj in result_list]
#
# 		else:
# 			print(price_range)
#
# 		ctx = {'loggedIn': False, 'item_list': pkg_list}
# 		if self.request.user.is_authenticated:
# 			ctx['loggedIn'] = True
# 		return ctx
#

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
		            url=str(pkg.id), rest_name=pkg.restaurant.restaurant_name)
		# ing_list = list(IngredientList.objects.all().filter(pack_id=id).values('ingr_id'))
		# print(pkg.get_absolute_url())
		ctx = {'loggedIn': False, 'item': pkg, 'item_img': [pkg.img]}
		if self.request.user.is_authenticated:
			ctx['loggedIn'] = True
		return ctx


class checkoutView(TemplateView):
	template_name = 'browse/checkout.html'

	# def get(self, request, *args, **kwargs):
	# 	if self.request.user.is_authenticated:
	# 		return redirect('/')
	# 	else:
	# 		return super().get(request, *args, **kwargs)
	# 
	# def get_context_data(self, **kwargs):
	# 	ctx = super(BranchRegisterView, self).get_context_data(**kwargs)
	# 	ctx['user_form'] = UserForm(prefix='user')
	# 	# ctx['profile_form'] = ProfileForm(prefix='profile')
	# 	ctx = {'loggedIn': False}
	# 	if self.request.user.is_authenticated:
	# 		print('Logged in: ' + str(self.request.user))
	# 		ctx['loggedIn'] = True
	# 	return ctx
	# 
	# def post(self, request, *args, **kwargs):
	# 	print(pretty_request(request))
	# 
	# 	if request.POST.get('password') != request.POST.get('re_pass'):
	# 		return
	# 
	# 	user_form = UserForm(request.POST)
	# 	user = None
	# 	branch = RestaurantBranch()
	# 	try:
	# 
	# 		rest = Restaurant.objects.get(restaurant_key=request.POST['rest_key'])
	# 		if user_form.is_valid():
	# 			user = user_form.save(commit=False)
	# 			user.is_manager = True
	# 			# branch_form = RestaurantBranchForm(request.POST)
	# 			# print('here')
	# 			# if branch_form.is_valid():
	# 			# 	branch = branch_form.save(commit=False)
	# 			# 	print(branch_form)
	# 			#
	# 			# 	print(branch)
	# 			user.save()
	# 
	# 			print(rest)
	# 
	# 			branch.user = user
	# 			branch.restaurant_id = rest
	# 			# print(branch.restaurant_id)
	# 			branch.branch_location = request.POST['lat'] + ',' + request.POST['lon']
	# 			print(branch.branch_location)
	# 
	# 			branch.branch_name = request.POST['branch_name']
	# 			print(branch.branch_name)
	# 			try:
	# 				branch.branch_location_details = request.POST['extra_details']
	# 			except Exception:
	# 				pass
	# 			# branch.location_area = ...
	# 			branch.save()
	# 			login(request, user)
	# 		# UserProfile.objects.create(user=user).save() # lagbe na i guess
	# 		else:
	# 			return HttpResponse("Invalid Form or pass")
	# 	except Exception as e:
	# 		print(e)
	# 		return HttpResponse('Not Valid secret key')

class RestaurantList(ListView):
	template_name = 'browse/restaurants.html'
	queryset = Restaurant.objects.exclude(restaurant_key='0')
	context_object_name = 'restaurants'
# print(queryset)
