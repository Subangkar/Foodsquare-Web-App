import re

from django.http import HttpResponse
from django.shortcuts import redirect

from django.views.generic import TemplateView

from accounts.forms import UserForm, RestaurantForm

from accounts.models import *
from browse.forms import PackageForm
from browse.models import Ingredient, IngredientList


class IndexView(TemplateView):
	template_name = 'manager/index.html'

	def get_context_data(self, **kwargs):
		context = {'loggedIn': self.request.user.is_authenticated}
		return context

	def post(self, request, *args, **kwargs):
		pass


class ProcessOrdersView(TemplateView):
	template_name = 'manager/manage_order.html'

	def get_context_data(self, **kwargs):
		# rests = Rest
		branch = RestaurantBranch.objects.get(user=self.request.user)
		obj_list = Order.objects.filter(branch=branch)#.order_by('status', '-time')
		print(branch)
		print(obj_list)
		print('-----')
		return {'object_list': obj_list}


class EditRestaurantView(TemplateView):
	template_name = 'manager/edit_restaurant.html'

	def get(self, request, *args, **kwargs):
		if request.user.is_branch_manager:
			return redirect('/orders/')
		return super(self.__class__, self).get(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(EditRestaurantView, self).get_context_data(kwargs=kwargs)
		print(context)
		# if self.request.user.is_branch_manager:
		# 	self.template_name = 'manager/manage_order.html'
		# pass
		# elif self.request.user.is_manager:
		context['restaurant'] = User.objects.get(id=self.request.user.id).restaurant
		# pass
		return context

	def post(self, request, *args, **kwargs):
		print(request)
		oldUser = User.objects.get(id=request.user.id)
		user_form = UserForm(request.POST, oldUser)
		profile = User.objects.get(id=self.request.user.id).restaurant
		profile.user = oldUser
		profile_form = RestaurantForm(
			request.POST or None, request.FILES or None, instance=profile)
		print(profile_form)
		if profile_form.is_valid():
			profile_form.save()
			print('Registering : ' + str(request.user))
			return HttpResponse("Signed Up!<br><a href='/'>Go to home</a>")
		# if user_form.is_valid():
		# user = user_form.save(commit=False)
		# user.save()

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
		oldUser = User.objects.get(id=request.user.id)
		user_form = UserForm(request.POST, oldUser)
		restaurant = User.objects.get(id=self.request.user.id).restaurant
		print(request.POST)
		menu_form = PackageForm(
			request.POST or None, request.FILES or None)
		# print(menu_form)
		ingrd_list = request.POST.getlist('ingrds')[0].split(',')

		if menu_form.is_valid():
			menu = menu_form.save(commit=False)
			menu.restaurant = restaurant
			print(menu)
			menu.save()
			for tmp in ingrd_list:
				tmp = " ".join(re.sub('[^a-zA-Z]+', ',', tmp.lower()).split(','))
				ingrd, created = Ingredient.objects.get_or_create(name=tmp)
				IngredientList.objects.create(pack_id=menu, ingr_id=ingrd)
			return HttpResponse("<h1>Menu Added Up</h1>")

		else:
			return HttpResponse("Error : <a href='/signup'>Try again</a>!")
		pass
