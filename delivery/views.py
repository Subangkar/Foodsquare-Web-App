import json
import re

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from django.views.generic import TemplateView

from accounts.forms import UserForm, RestaurantForm

from accounts.models import *
from accounts.utils import pretty_request
from browse.forms import PackageForm
from browse.models import Ingredient, IngredientList
from delivery.utils_db import *


class IndexView(TemplateView):
	template_name = 'delivery/index.html'

	def get_context_data(self, **kwargs):
		context = {'loggedIn': self.request.user.is_authenticated}
		return context


class AcceptOrdersView(TemplateView):
	template_name = 'delivery/delivery_order.html'

	def get_context_data(self, **kwargs):
		# obj_list = Order.objects.filter(branch__location_area__iexact=self.request.user.deliveryman.address)
		obj_list = get_next_orders(self.request.user.id) | get_taken_orders(self.request.user.id)
		return {'object_list': obj_list}


class EditProfileView(TemplateView):
	template_name = 'delivery/EditProfile.html'

	def get(self, request, *args, **kwargs):
		return super(self.__class__, self).get(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(EditProfileView, self).get_context_data(**kwargs)
		print(pretty_request(self.request))
		context['userprofile'] = User.objects.get(id=self.request.user.id).deliveryman

		return context

	def post(self, request, *args, **kwargs):
		# print(request)
		# oldUser = User.objects.get(id=request.user.id)
		# user_form = UserForm(request.POST, oldUser)
		# profile = oldUser.userprofile
		# profile.user = oldUser
		# profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
		# print(profile_form)
		# if profile_form.is_valid():
		# 	profile_form.save()
		# 	print('Registering : ' + str(request.user))
		# 	return HttpResponse("Signed Up!<br><a href='/'>Go to home</a>")
		# # if user_form.is_valid():
		# # user = user_form.save(commit=False)
		# # user.save()
		#
		# else:
		# 	return HttpResponse("Error : <a href='/signup'>Try again</a>!")
		# # menuForm = MenuForm(request.POST or None, request.FILES or None)
		# # menuForm.save()
		# # print(menuForm)
		# # return HttpResponse("<h1>Congrats</h1>")
		pass


def acceptDelivery(request):
	print(request)
	order_id = request.POST.get('order_id')
	deliveryman = DeliveryMan.objects.get(user=request.user)
	print(order_id)
	print(deliveryman)
	status = request.POST.get('delivery_option')
	order = Order.objects.get(id=order_id)
	if status == 'take':
		if order.order_status != Order.PROCESSING:
			return JsonResponse({"accepted": False})
		order.assignDeliveryman(deliveryman)
		from customer.utils_db import send_notification
		send_notification(order.user.id, "Your order: " + str(
			order.id) + " from " + order.branch.branch_name + " has been proceeded to deliver.\n"
		                                                      "Wait for deliveryman to reach at your delivery address.")

	elif status == 'deliver':
		order.submitDelivery()
		from customer.utils_db import send_notification
		send_notification(order.user.id, "Your order: " + str(
			order.id) + " from " + order.branch.branch_name + " was delivered to your delivery address.")

	return JsonResponse({"accepted": True})


def delivery_details(request):
	"""
	given an order id, find order details i.e. which item in which quantity and give total price
	"""
	id = request.GET.get('id')
	pkg_list, order, price, deliver_charge = get_order_details(id)
	print(order.delivery)
	return render(request, 'delivery/delivery_modal.html',
	              {'item_list': pkg_list, 'order': order, 'price': price, 'delivery_charge': deliver_charge})


class Delivered_Orders(TemplateView):
	template_name = 'delivery/previous_order.html'

	def get_context_data(self, **kwargs):
		# obj_list = Order.objects.filter(branch__location_area__iexact=self.request.user.deliveryman.address)
		obj_list = get_past_orders(self.request.user.id)
		return {'object_list': obj_list}


def submitCustomerRating(request):
	submit_rating(order_id=request.POST.get('order-id'), rating=request.POST.get('rating'))
	return True
