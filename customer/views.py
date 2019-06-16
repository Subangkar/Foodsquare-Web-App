from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
# Create your views here.
from django.views.generic import TemplateView
from django.views.generic.base import View

from accounts.utils import pretty_request


class EditProfileView(TemplateView):
	template_name = 'customer/EditProfile.html'

	def get(self, request, *args, **kwargs):
		return super(self.__class__, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		# menuForm = MenuForm(request.POST or None, request.FILES or None)
		# menuForm.save()
		# print(menuForm)
		# return HttpResponse("<h1>Congrats</h1>")
		pass