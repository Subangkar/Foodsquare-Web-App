from django.shortcuts import render

# Create your views here.
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView
from browse.utils import *


# from .serializers import *


def index(request):
	return render(request, "browse/index.html", {})


def viewOrder(request):
	return render(request, "browse/order.html")


def viewRestaurants(request):
	return render(request, "browse/restaurants.html", {})


class Index(TemplateView):
	template_name = 'browse/index.html'

	def get_context_data(self, **kwargs):
		with open("sessionLog.txt", "a") as myfile:
			myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")
		# print(self.request.GET)
		# print(self.request.user)
		# print(self.request.user.is_authenticated)
		ctx = {'loggedIn': False}
		if self.request.user.is_authenticated:
			ctx['loggedIn'] = True
		return ctx


class Order(TemplateView):
	template_name = 'browse/order.html'

	def get_context_data(self, **kwargs):
		with open("sessionLog.txt", "a") as myfile:
			myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")
		# print(self.request.GET)
		# print(self.request.user)
		# print(self.request.user.is_authenticated)
		ctx = {'loggedIn': False}
		if self.request.user.is_authenticated:
			ctx['loggedIn'] = True
		return ctx
