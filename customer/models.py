from django.db import models


class Notification(models.Model):
	"""Notifications for any system user"""
	message = models.CharField(verbose_name="Message", max_length=250, blank=False, null=False)
	time = models.DateTimeField(verbose_name="Notification Push Time", auto_now_add=True)
	read = models.BooleanField(verbose_name="Notification has been read", default=False)
	read_time = models.DateTimeField(verbose_name="Notification read time", auto_now_add=False, null=True)

	user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name="notification_target_user")

	def mark_as_read(self):
		from datetime import datetime
		self.read = True
		self.read_time = datetime.now()
		self.save()

	@staticmethod
	def send_notification(user, text):
		notification = Notification(user=user, message=text)
		notification.save()
		user.notificationmonitor.last_push_time = notification.time
		user.notificationmonitor.save()

	@staticmethod
	def get_new_notifications(user):
		from datetime import datetime
		notifications = Notification.objects.filter(user=user,
		                                            time__gt=user.notificationmonitor.last_pop_time).order_by(
			'-time')
		user.notificationmonitor.last_pop_time = datetime.now()
		user.notificationmonitor.save()
		return notifications

	@staticmethod
	def get_unread_notifications(user):
		return Notification.objects.filter(user=user, read=False).order_by('-time')

	@staticmethod
	def get_all_notifications(user, time=None):
		""" Get all notifications arrived after provided time at descending order """
		return Notification.objects.filter(user=user, time__gt=time).order_by('-time')


class NotificationMonitor(models.Model):
	user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
	last_push_time = models.DateTimeField(verbose_name="Last Pushed Timestamp", auto_now_add=True)
	last_pop_time = models.DateTimeField(verbose_name="Last Popped Timestamp", auto_now_add=True)

	def has_new_notification(self):
		return self.last_pop_time < self.last_push_time


def test():
	pass
	from accounts.models import User
	# from customer.models import *
	user = User.objects.get(id=2)
	Notification.get_unread_notifications(user)
	from customer.utils_db import send_notification
	send_notification(2, "You have a new notification")
	Notification.get_new_notifications(user)
