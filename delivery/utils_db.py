def get_order_details(order_id):
	"""
	:return: (packages_in_order, total_package_price, delivery_charge)
	"""
	from accounts.models import Order
	order = Order.objects.get(id=order_id)
	if order:
		pkg_list = order.get_package_list()
		total_package_price = sum(pack.price for pack in pkg_list)
		delivery_charge = order.payment.price - total_package_price
		return pkg_list, order, total_package_price, delivery_charge


def get_next_orders(user_id):
	from accounts.models import User, Order
	user = User.objects.get(id=user_id)
	if user and user.is_delivery_man:
		orders = Order.objects.filter(order_status=Order.PROCESSING,
		                              branch__location_area__iexact=user.deliveryman.address)
		return orders


def get_taken_orders(user_id):
	from accounts.models import User, Order
	user = User.objects.get(id=user_id)
	if user and user.is_delivery_man:
		orders = Order.objects.filter(order_status=Order.DELIVERING, delivery__deliveryman__user=user)
		return orders


def get_past_orders(user_id):
	from accounts.models import User, Order
	user = User.objects.get(id=user_id)
	if user and user.is_delivery_man:
		orders = Order.objects.filter(order_status=Order.DELIVERED, delivery__deliveryman__user=user)
		return orders


def submit_rating(order_id, rating=5):
	from accounts.models import Order
	order = Order.objects.get(id=order_id)
	order.delivery.rating_user = rating
	order.delivery.save()


def get_nearest_branches(user_id):
	from accounts.models import User
	user = User.objects.get(id=user_id)
	from accounts.models import RestaurantBranch
	return RestaurantBranch.objects.filter(location_area__iexact=user.deliveryman.address)


# ---------------- Rating ----------------------

def get_avg_deliveryman_rating(user_id):
	from accounts.models import Order
	from django.db.models import Avg
	return Order.objects.filter(delivery__deliveryman__user__id=user_id).aggregate(Avg('delivery__rating_deliveryman'))[
		'delivery__rating_deliveryman__avg']


# ---------------- Just for DB ----------------------

def delete_order(id):
	from accounts.models import Order, OrderPackageList
	order = Order.objects.filter(id=id)
	OrderPackageList.objects.filter(order__id=id).delete()
	order.delivery.delete()
	order.payment.delete()
	order.delete()
