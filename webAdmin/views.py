import json

from django.core import serializers
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView, ListView

from accounts.models import Order, RestaurantBranch
from browse.models import Package
from webAdmin.utils import *


class RestaurantListView(ListView):
	template_name = 'webAdmin/restaurant_list.html'
	queryset = Restaurant.objects.all()
	context_object_name = 'restaurants'
	paginate_by = 10


def requestAccept(request, id):
	obj = Restaurant.objects.get(id=id)
	obj.restaurant_key = uniqueKey()
	user = obj.user
	send_mail(
		'Account Activated',
		'You Restaurant Account has been activated.\n ' +
		'Username:' + user.username + '\n ' +
		'Restaurant:' + obj.restaurant_name + '\n ' +
		'Your Key:' + obj.restaurant_key + '\n ' +
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
	paginate_by = 10


class AdminDashBoardView(TemplateView):
	template_name = 'webAdmin/admin_dashboard.html'

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated or not request.user.is_superuser:
			return redirect(reverse('index'))

		return super(self.__class__, self).get(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(AdminDashBoardView, self).get_context_data(kwargs=kwargs)
		if self.request.user.is_authenticated and self.request.user.is_superuser:
			from django.utils.timezone import datetime
			today = datetime.today()
			context['order_cnt'] = Order.objects.filter(time__month=today.month, time__year=today.year).count()
			context['monthly_revenue'] = sum(
				pkg.price for ord in Order.objects.filter(time__month=today.month, time__year=today.year) for pkg in
				ord.get_package_list())
			context['item_cnt'] = Package.objects.filter(available=True).count()
			context['rest_count'] = Restaurant.objects.exclude(restaurant_key='0').count()
			context['user_cnt'] = User.objects.filter(is_customer=True).count()
			context['months'] = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
			                     "October", "November", "December"]
			context['restaurants'] = get_monthwise_order_completed_count_all()
			context['menus'] = get_packagewise_order_completed_count_all(last_n_months=3)
		return context


def get_notifications(request):
	from customer.utils_db import get_unread_notifications
	unreads = get_unread_notifications(request.user)
	if unreads is not None:
		notifications = [notf.message for notf in unreads]
	else:
		notifications = []
	return JsonResponse({'notifications': notifications})


def read_notifications(request):
	from datetime import datetime
	from customer.utils_db import read_all_notifications
	read_all_notifications(request.user, datetime.now())
	return JsonResponse({'Success': True})


def branch_list(request):
	id = request.GET.get('id')
	branch_list = RestaurantBranch.objects.filter(restaurant__id=id)

	return render(request, 'webAdmin/branch_info.html', {'branchList': branch_list})


class BlockedUsersView(ListView):
	template_name = 'webAdmin/blocked_user.html'
	context_object_name = 'customers'
	paginate_by = 10

	def get_queryset(self):
		return User.objects.filter(is_customer=True, is_suspended=True)


class BlockedDeliveryMenView(ListView):
	template_name = 'webAdmin/blocked_user.html'
	context_object_name = 'customers'
	paginate_by = 10

	def get_queryset(self):
		return User.objects.filter(is_delivery_man=True, is_suspended=True).order_by('-last_login')


class EditConfigView(TemplateView):
	template_name = 'webAdmin/configuration.html'

	def get_context_data(self, *args, **kwargs):
		return {'settings': Config.objects.all()}

	def post(self, request, *args, **kwargs):
		print(self.request.POST)
		from copy import copy
		post_data = copy(self.request.POST)
		del post_data['csrfmiddlewaretoken']
		for k in post_data:
			Config.set_value(k, post_data[k].strip())
		return redirect('/editConfiguration/')


def unblock(request):
	id = request.GET.get('id')
	user = User.objects.get(id=id)
	user.active_account()
	return JsonResponse({'accepted': True})
