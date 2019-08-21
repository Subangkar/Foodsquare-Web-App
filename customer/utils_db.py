from customer.models import *


def send_notification(user, text):
	from accounts.models import User
	if User.objects.filter(user=user).exists() and text != "":
		Notification.send_notification(user, text)


def get_new_notifications(user):
	return Notification.get_new_notifications(user)


def get_unread_notifications(user):
	return Notification.get_unread_notifications(user)


def get_all_notifications(user, time=None):
	""" Get all notifications arrived after provided time at descending order """
	return Notification.get_all_notifications(user, time)
