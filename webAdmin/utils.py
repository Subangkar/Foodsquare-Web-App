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