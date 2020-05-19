from django.db import models


class Config(models.Model):
	"""Settings database"""
	key = models.CharField(verbose_name='Configuration Type', max_length=50, unique=True, null=False)
	value = models.CharField(verbose_name='Configuration Value', max_length=100)

	DELIVERY_CHARGE_PERCENTAGE = 'delivery_charge'
	ITEMS_PER_PAGE = 'items_per_page'
	SETTINGS = ((DELIVERY_CHARGE_PERCENTAGE, 'delivery_charge'), (ITEMS_PER_PAGE, 'items_per_page'))
	ACCOUNT_SUSPEND_CONTACT = 'account_suspend_email'

	@staticmethod
	def set_value(settings, value):
		config, created = Config.objects.get_or_create(key=settings)
		config.value = str(value)
		config.save()
		if created:
			print('added settings ', config)

	@staticmethod
	def get_value(settings):
		if not Config.objects.filter(key=settings).exists():
			Config.set_value(settings, 9)
		return Config.objects.get(key=settings).value
