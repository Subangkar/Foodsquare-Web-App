# Create your views here.

from django.shortcuts import render
# from .serializers import *
from django.views.generic import TemplateView
from browse.utils import *


def viewRestaurants(request):
	return render(request, "browse/restaurants.html", {})


# for debug purpose only
def viewRaw(request):
	return render(request, "browse/toys_shop/base-banner.html", {})


class Index(TemplateView):
	template_name = 'browse/toys_shop/index.html'

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
	template_name = 'browse/toys_shop/order.html'

	def get_context_data(self, **kwargs):
		with open("sessionLog.txt", "a") as myfile:
			myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")
		item = item_t('toys(barbie)', 'browse/toys_shop/images/a1.jpg', '$575.00', '5', '/browse/item/')
		ctx = {'loggedIn': False, 'item_list': [item, item, item, item]}
		if self.request.user.is_authenticated:
			ctx['loggedIn'] = True
		return ctx


class Item(TemplateView):
	template_name = 'browse/toys_shop/item.html'

	def get_context_data(self, **kwargs):
		with open("sessionLog.txt", "a") as myfile:
			myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")
		ctx = {'loggedIn': False, 'item_img': [], 'reviewer_img': '/browse/toys_shop/images/team1.jpg'}
		ctx['item_img'] = ['/browse/toys_shop/images/f1.jpg', '/browse/toys_shop/images/f2.jpg',
		                   '/browse/toys_shop/images/f3.jpg']
		if self.request.user.is_authenticated:
			ctx['loggedIn'] = True
		return ctx
