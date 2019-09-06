import random
import string

from accounts.models import Restaurant


def uniqueKey(N=10):
	while True:
		key = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=N))
		if not Restaurant.objects.filter(restaurant_key=key).exists():
			return key


def get_delivery_charge(total_price):
	return 0.1 * total_price


def get_deliverymen_list():
	"""
	:return: charges of only current month
	"""
	from browse.utils_db import namedtuplefetchall
	query = "select delman.id,\
			       delman.name,\
			       delman.user_id,\
			       delman.address,\
			       count(delivery.id) as order_cnt,\
			       sum(delivery.charge) as payment\
			from accounts_deliveryman delman\
			         join accounts_delivery delivery on delman.id = delivery.deliveryman_id\
			         join accounts_order on delivery.id = accounts_order.delivery_id\
			where accounts_order.time >= date_trunc('month', CURRENT_DATE)\
			group by delman.id"
	return namedtuplefetchall(query, [])
