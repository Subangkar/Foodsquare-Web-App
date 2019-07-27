import re

from django.http import HttpResponse
from django.shortcuts import redirect

from django.views.generic import TemplateView

from accounts.forms import UserForm, RestaurantForm

from accounts.models import *
from browse.forms import PackageForm
from browse.models import Ingredient, IngredientList


class IndexView(TemplateView):
	template_name = 'delivery/index.html'

	def get_context_data(self, **kwargs):
		context = {'loggedIn': self.request.user.is_authenticated}
		return context

	def post(self, request, *args, **kwargs):
		pass


class AcceptOrdersView(TemplateView):
	template_name = 'delivery/delivery_order.html'

	def get_context_data(self, **kwargs):
		# rests = Rest
		obj_list = Order.objects.all()
		# print(obj_list)
		branch = 1
		print('-----')
		return {'object_list': obj_list, 'branch':  branch}


class EditProfileView(TemplateView):
	template_name = 'customer/EditProfile.html'

	def get(self, request, *args, **kwargs):

		return super(self.__class__, self).get(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(EditProfileView, self).get_context_data(**kwargs)
		print(pretty_request(self.request))
		try:
			obj = dict()
			context['userprofile'] = User.objects.get(id=self.request.user.id).userprofile
			context['socialacnt'] = False

		except Exception as e:
			obj = dict()
			obj = SocialAccount.objects.get(user_id=self.request.user.id).extra_data
			context['socialacnt'] = True
			try:  # for facebook
				obj['avatar'] = obj['picture']
				del obj['picture']
			except Exception as e1:
				pass
			context['userprofile'] = obj
			print(context)
		return context

	def post(self, request, *args, **kwargs):
		print(request)
		oldUser = User.objects.get(id=request.user.id)
		user_form = UserForm(request.POST, oldUser)
		profile = oldUser.userprofile
		profile.user = oldUser
		profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
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
		# menuForm = MenuForm(request.POST or None, request.FILES or None)
		# menuForm.save()
		# print(menuForm)
		# return HttpResponse("<h1>Congrats</h1>")
		pass

