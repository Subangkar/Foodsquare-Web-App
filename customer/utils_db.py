from customer.models import *


def send_notification(user_id, text):
	"""Sends a notification to user with given id with that text"""
	from accounts.models import User
	if User.objects.filter(id=user_id).exists() and text != "":
		Notification.send_notification(User.objects.get(id=user_id), text)


def get_unread_notifications(user):
	""" Get unread notifications at descending order of time """
	if user.is_authenticated:
		return user.get_unread_notifications()


def get_all_notifications(user, time=None):
	""" Get all notifications arrived after provided time at descending order """
	if user.is_authenticated:
		return Notification.get_all_notifications(user, time)


def read_all_notifications(user, time):
	""" Mark all notifications before provided time as read """
	if user.is_authenticated:
		user.read_notifications(time)


# ---------------- Delivery ----------------------

def submitDeliveryRating(order_id, rating):
	from accounts.models import Order
	order = Order.objects.get(order_id)
	order.delivery.rating_deliveryman = rating
	order.delivery.save()


def get_avg_customer_rating(user_id):
	from accounts.models import Order
	from django.db.models import Avg
	return Order.objects.filter(user__id=user_id).aggregate(Avg('delivery__rating_user'))['delivery__rating_user__avg']
