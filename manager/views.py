from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
# Create your views here.
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.contrib.auth.models import User

from accounts.forms import UserForm, ProfileForm
from accounts.utils import pretty_request
from browse.models import Ingredient
from .forms import MenuForm


class IndexView(TemplateView):
	template_name = 'manager/index.html'

	def get_context_data(self, **kwargs):
		context = {'loggedIn': False}
		if self.request.user.is_authenticated:
			context['loggedIn'] = True
		return context

	def post(self, request, *args, **kwargs):
		pass


class HomepageView(TemplateView):
	template_name = 'manager/manager_profile.html'

	def get(self, request, *args, **kwargs):
		return super(self.__class__, self).get(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(HomepageView, self).get_context_data()
		context['ingredient_list'] = Ingredient.objects.all()
		return context

	def post(self, request, *args, **kwargs):
		pass

