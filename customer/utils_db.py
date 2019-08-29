from customer.models import *


def send_notification(user_id, text):
	"""Sends a notification to user with given id with that text"""
	from accounts.models import User
	if User.objects.filter(id=user_id).exists() and text != "":
		Notification.send_notification(User.objects.get(id=user_id), text)


def get_new_notifications(user):
	""" Get new notifications which never has been sent to user at descending order of time """
	from accounts.models import User
	if user.is_authenticated and user.is_customer:
		return Notification.get_new_notifications(user)


def get_unread_notifications(user):
	""" Get unread notifications at descending order of time """
	from accounts.models import User
	if user.is_authenticated and user.is_customer:
		return Notification.get_unread_notifications(user)


def get_all_notifications(user, time=None):
	""" Get all notifications arrived after provided time at descending order """
	from accounts.models import User
	if user.is_authenticated and user.is_customer:
		return Notification.get_all_notifications(user, time)


def read_all_notifications(user, time):
	""" Mark all notifications before provided time as read """
	from accounts.models import User
	if user.is_authenticated and user.is_customer:
		for notf in Notification.objects.filter(user=user, time__lte=time):
			notf.mark_as_read()
			print(notf)


# ---------------- Delivery ----------------------

def submitDeliveryRating(order_id, rating):
	from accounts.models import Order
	order = Order.objects.get(order_id)
	order.delivery.rating_deliveryman = rating
	order.delivery.save()
