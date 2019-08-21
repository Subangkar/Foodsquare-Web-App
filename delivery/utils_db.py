def get_order_details(order_id):
	"""
	:return: (packages_in_order, total_package_price, delivery_charge)
	"""
	from accounts.models import Order
	order = Order.objects.get(id=order_id)
	if order:
		pkg_list = order.get_package_list()
		total_package_price = sum(pack.package.price * pack.quantity for pack in pkg_list)
		delivery_charge = order.payment.price - total_package_price
		return pkg_list,order, total_package_price, delivery_charge
