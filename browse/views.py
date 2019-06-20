# Create your views here.

from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from browse.utils import *
from manager.models import Menu


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

	def get(self, request, *args, **kwargs):
		if kwargs.get('id') is None or not isinstance(kwargs['id'], int):
			return redirect('/order/')
		return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		with open("sessionLog.txt", "a") as myfile:
			myfile.write(">>>>>>\n" + pretty_request(self.request) + "\n>>>>>>\n")
		id = kwargs['id']
		itm = Menu.objects.get(id=id)
		item = item_t(name=itm.menu_name, price="$" + str(itm.price), img=itm.menu_img, rating='5',
		              url="/browse/item/" + str(itm.id))

		ctx = {}
		if self.request.user.is_authenticated:
			ctx['loggedIn'] = True
			ctx['item'] = item
			ctx['item_img'] = [item.img]
		return ctx
