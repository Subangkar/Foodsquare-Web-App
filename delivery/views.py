from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView

from accounts.models import *
from accounts.utils import pretty_request
from delivery.utils_db import *


class IndexView(TemplateView):
	template_name = 'delivery/index.html'

	def get(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('/orders/')
		return super(self.__class__, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = {'loggedIn': self.request.user.is_authenticated}
		return context


class AcceptOrdersView(ListView):
	template_name = 'delivery/delivery_order.html'
	context_object_name = 'object_list'
	paginate_by = 10

	def get_queryset(self):
		print(self.request.user.id)
		obj_list = get_next_orders(self.request.user.id) | get_taken_orders(self.request.user.id)
		return obj_list


class EditProfileView(TemplateView):
	template_name = 'delivery/EditProfile.html'

	def get_context_data(self, *args, **kwargs):
		context = super(EditProfileView, self).get_context_data(**kwargs)
		print(pretty_request(self.request))
		context['userprofile'] = User.objects.get(id=self.request.user.id).deliveryman
		context['locations'] = set([x.location_area for x in RestaurantBranch.objects.raw("select * from accounts_restaurantbranch \
				where location_area notnull and location_area!=\'\'")])
		return context


def acceptDelivery(request):
	print(request)
	order_id = request.POST.get('order_id')
	deliveryman = DeliveryMan.objects.get(user=request.user)
	print(order_id)
	print(deliveryman)
	if order_id is None:
		return JsonResponse({"accepted": False})
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
		send_notification(request.user.id,
						  "You accepted delivery for order id:" + str(
							  order.id) + " to deliver to " + order.user.username)

	elif status == 'deliver':
		order.submitDelivery()
		from customer.utils_db import send_notification
		send_notification(order.user.id, "Your order: " + str(
			order.id) + " from " + order.branch.branch_name + " was delivered to your delivery address.")
		send_notification(request.user.id, "You delivered order id:" + str(order.id) + " to " + order.user.username)

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


class Delivered_Orders(ListView):
	template_name = 'delivery/previous_order.html'
	context_object_name = 'object_list'
	paginate_by = 10

	def get_queryset(self):
		obj_list = get_past_orders(self.request.user.id)
		return obj_list


def submitCustomerRating(request):
	print(request.POST.get('order-id'))
	print(int(request.POST.get('rating')))
	submit_rating(order_id=request.POST.get('order-id'), rating=int(request.POST.get('rating')))
	return True


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
