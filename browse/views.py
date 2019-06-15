# Create your views here.

from django.shortcuts import render
from django.views.generic import TemplateView
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
		ctx = {'loggedIn': False}
		if self.request.user.is_authenticated:
			ctx['loggedIn'] = True
		return ctx


class item_t:
	def __init__(self, name='', img='', price='', rating='', url='/'):
		self.name = name
		self.img = img
		self.price = price
		self.rating = range(int(rating))
		self.url = url


class Order(TemplateView):
	template_name = 'browse/order.html'

	def get_context_data(self, **kwargs):
		with open("sessionLog.txt", "a") as myfile:
			myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")
		item = item_t('toys(barbie)', 'browse/images/cuisine2.jpg', '$575.00', '5', '/browse/item/')
		ctx = {'loggedIn': False, 'item_list': [item, item, item, item]}
		if self.request.user.is_authenticated:
			ctx['loggedIn'] = True
		return ctx


class Item(TemplateView):
	template_name = 'browse/item.html'

	def get_context_data(self, **kwargs):
		with open("sessionLog.txt", "a") as myfile:
			myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")
		ctx = {'loggedIn': False, 'item_img': [], 'reviewer_img': '/browse/images/toys_shop/team1.jpg'}
		ctx['item_img'] = ['/browse/images/cuisine1.jpg', '/browse/images/cuisine2.jpg',
		                   '/browse/images/cuisine3.jpg']
		if self.request.user.is_authenticated:
			ctx['loggedIn'] = True
		return ctx
