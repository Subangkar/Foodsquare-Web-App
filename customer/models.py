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

	@staticmethod
	def get_unread_notifications(user):
		return Notification.objects.filter(user=user, read=False).order_by('-time')

	@staticmethod
	def get_all_notifications(user, time=None):
		""" Get all notifications arrived after provided time at descending order """
		return Notification.objects.filter(user=user, time__gt=time).order_by('-time')
