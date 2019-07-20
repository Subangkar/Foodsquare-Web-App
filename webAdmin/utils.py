import random
import string

from accounts.models import Restaurant


def uniqueKey(N=10):
	while True:
		key = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=10))
		if not Restaurant.objects.filter(restaurant_key=key).exists():
			return key
