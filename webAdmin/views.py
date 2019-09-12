from django.core import serializers
import json

from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import TemplateView, ListView

from accounts.models import Restaurant, Order
from browse.models import Package
from webAdmin.utils import uniqueKey, get_deliverymen_list


class RestaurantListView(ListView):
	template_name = 'webAdmin/restaurant_list.html'
	queryset = Restaurant.objects.all()
	context_object_name = 'restaurants'


def requestAccept(request, id):
	obj = Restaurant.objects.get(id=id)
	obj.restaurant_key = uniqueKey()
	user = obj.user
	send_mail(
		'Account Activated',
		'You Restaurant Account has been activated.<br>' +
		'Username:' + user.username + '<br>' +
		'Restaurant:' + obj.restaurant_name + '<br>' +
		'Your Key:' + obj.restaurant_key + '<br>' +
		'You can now login with your username and password at.',
		'accounts@foodsquare',
		[obj.user.email],
		fail_silently=False,
	)
	obj.save()
	return redirect('/homepage/')


def restaurantDetails(request):
	id = request.GET.get('id')
	obj = Restaurant.objects.get(id=id)
	ser = serializers.serialize('json', [obj])
	json_obj = json.loads((ser.strip('[]')))
	print(json_obj['fields'])
	return JsonResponse(json_obj['fields'])


class DeliveyListView(ListView):
	template_name = 'webAdmin/delivery_info.html'
	queryset = get_deliverymen_list()
	context_object_name = 'delivery_men'


class AdminDashBoardView(TemplateView):
	template_name = 'webAdmin/admin_dashboard.html'

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect(reverse('index'))

		return super(self.__class__, self).get(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(AdminDashBoardView, self).get_context_data(kwargs=kwargs)
		if self.request.user.is_authenticated and self.request.user.is_manager:
			import datetime
			today = datetime.date.today()
			context['order_cnt'] = Order.objects.filter(branch__restaurant=self.request.user.restaurant,
			                                            time__month=today.month, time__year=today.year).count()
			context['monthly_revenue'] = sum(pkg.price for ord in
			                                 Order.objects.filter(branch__restaurant=self.request.user.restaurant,
			                                                      time__month=today.month) for pkg in
			                                 ord.get_package_list())
			context['item_cnt'] = Package.objects.filter(restaurant=self.request.user.restaurant,
			                                             available=True).count()

		return context


def get_notifications(request):
	return None


def read_notifications(request):
	return None