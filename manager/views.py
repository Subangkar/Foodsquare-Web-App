import re

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView

from accounts.forms import RestaurantForm
from accounts.models import *
from browse.forms import PackageForm
from browse.models import Ingredient, IngredientList, PackageBranchDetails, Package


class IndexView(TemplateView):
	template_name = 'manager/index.html'

	def get(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect(reverse('homepage'))
		return super(self.__class__, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = {'loggedIn': self.request.user.is_authenticated}
		return context


class ProcessOrdersView(TemplateView):
	template_name = 'manager/manage_order.html'

	def get_context_data(self, **kwargs):
		branch = RestaurantBranch.objects.get(user=self.request.user)
		obj_list = Order.objects.filter(branch=branch)  # .order_by('status', '-time')
		print(branch)
		print('-----')
		return {'object_list': obj_list, 'branch': branch}


class EditRestaurantView(TemplateView):
	template_name = 'manager/edit_restaurant.html'

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect(reverse('index'))
		if request.user.is_branch_manager:
			return redirect('/orders/')
		return super(self.__class__, self).get(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(EditRestaurantView, self).get_context_data(kwargs=kwargs)
		if self.request.user.is_authenticated and self.request.user.is_manager:
			context['restaurant'] = User.objects.get(id=self.request.user.id).restaurant
		return context

	def post(self, request, *args, **kwargs):
		print(request)
		profile = User.objects.get(id=self.request.user.id).restaurant
		profile.user = request.user
		profile_form = RestaurantForm(
			request.POST or None, request.FILES or None, instance=profile)
		print(profile_form)
		if profile_form.is_valid():
			profile_form.save()
			print('Registering : ' + str(request.user))
			return HttpResponse("Signed Up!<br><a href='/'>Go to home</a>")

		else:
			return HttpResponse("Error : <a href='/signup'>Try again</a>!")
		pass


class AddMenuView(TemplateView):
	template_name = 'manager/add_menu.html'

	def get(self, request, *args, **kwargs):
		return super(self.__class__, self).get(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(AddMenuView, self).get_context_data()
		context['ingredient_list'] = Ingredient.objects.all()
		return context

	def post(self, request, *args, **kwargs):
		restaurant = User.objects.get(id=self.request.user.id).restaurant
		print(request.POST)
		menu_form = PackageForm(request.POST or None, request.FILES or None)
		ingrd_list = request.POST.getlist('ingrds')[0].split(',')
		print(menu_form)
		if menu_form.is_valid():
			menu = menu_form.save(commit=False)
			menu.restaurant = restaurant
			print(menu)
			menu.save()
			for tmp in ingrd_list:
				tmp = " ".join(re.sub('[^a-zA-Z]+', ',', tmp.lower()).split(','))
				ingrd, created = Ingredient.objects.get_or_create(name=tmp)
				IngredientList.objects.create(pack_id=menu, ingr_id=ingrd)
			PackageBranchDetails.add_package_to_all_branches(restaurant=restaurant, package=menu)
			return HttpResponse("<h1>Menu Added Up</h1>")

		else:
			return HttpResponse("<h1>Error : <a href='/signup'>Try again</a>!<h1>")
		pass


class EditMenuView(TemplateView):
	template_name = 'manager/edit_menu.html'

	def get(self, request, *args, **kwargs):
		return super(self.__class__, self).get(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		""" Prevent Accessing Other Restaurants Package """
		id = kwargs['id']
		pkg = Package.objects.get(id=id)
		if not pkg.is_editable(self.request.user):
			pkg = None
			ing_list = None
		else:
			ing_list = [ingobj.ingr_id.name for ingobj in IngredientList.objects.filter(pack_id=pkg.id)]
		# comments = PackageReview.objects.filter(package=pkg)
		user_id = self.request.user.id if self.request.user.is_authenticated else 0
		ctx = {'loggedIn': self.request.user.is_authenticated, 'item': pkg, 'item_img': [pkg.image],
		       'ing_list': ing_list
		       }
		return ctx

	def post(self, request, *args, **kwargs):
		id = kwargs['id']

		pkg = Package.objects.get(id=id)
		if not pkg.is_editable(self.request.user):
			return HttpResponse("<h1>Access Error: Not permitted to edit for current user<h1>")
		restaurant = User.objects.get(id=self.request.user.id).restaurant
		print(request.POST)
		menu_form = PackageForm(request.POST or None, request.FILES or None, instance=pkg)
		ingrd_list = request.POST.getlist('ingrds')[0].split(',')
		print(menu_form)
		if menu_form.is_valid():
			menu = menu_form.save(commit=False)
			menu.restaurant = restaurant
			print(menu)
			menu.save()
			for tmp in ingrd_list:
				tmp = " ".join(re.sub('[^a-zA-Z]+', ',', tmp.lower()).split(','))
				ingrd, created = Ingredient.objects.get_or_create(name=tmp)
				IngredientList.objects.get_or_create(pack_id=menu, ingr_id=ingrd)
			PackageBranchDetails.add_package_to_all_branches(restaurant=restaurant, package=menu)
			return HttpResponse("<h1>Menu Added Up</h1>")

		else:
			return HttpResponse("<h1>Error : <a href='/signup'>Try again</a>!<h1>")
		pass


def DeliveryAvailability(request):
	print(request)
	id = request.POST.get('id')
	status = request.POST.get('delivery_option')
	print(id)
	branch = RestaurantBranch.objects.get(id=id)
	if status == 'close_delivery':
		branch.running = False
	else:
		branch.running = True

	branch.save()


def acceptOrder(request):
	order_id = request.POST.get('order_id')
	order = Order.objects.get(id=order_id)
	order.order_status = order.PROCESSING
	order.save()
	return JsonResponse({'order': 'placed'})


class ViewMenusView(TemplateView):
	template_name = 'manager/manage_menus.html'

	def get_context_data(self, **kwargs):
		restaurant = User.objects.get(id=self.request.user.id).restaurant
		obj_list = Package.objects.filter(restaurant=restaurant)  # .order_by('status', '-time')
		print(obj_list)
		print('-----')
		return {'menu_list': obj_list}
