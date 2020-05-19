import random
import string

from accounts.models import Restaurant, User
from webAdmin.models import Config


def uniqueKey(N=10):
	while True:
		key = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=N))
		if not Restaurant.objects.filter(restaurant_key=key).exists():
			return key


# ------------------ Configs ----------------------
def get_delivery_charge(total_price):
	return round(float(Config.get_value(Config.DELIVERY_CHARGE_PERCENTAGE)) / 100 * total_price, 2)


def get_delivery_charge_percentage():
	return round(float(Config.get_value(Config.DELIVERY_CHARGE_PERCENTAGE)) / 100, 2)


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


def get_no_items_per_page():
	return Config.get_value(Config.ITEMS_PER_PAGE)


def send_notification_to_admin(message):
	admins = User.objects.filter(is_superuser=True)
	if not admins.exists():
		return
	for admin in admins:
		from customer.utils_db import send_notification
		send_notification(admin.id, message)


# ---------------------- Dashboard -----------------------------

def get_monthwise_order_completed_count_all():
	"""monthwise order completed restaurant wise top 3 only"""
	from browse.utils_db import namedtuplefetchall
	query = "select restaurant.restaurant_name                       as name,\
					to_char(date_trunc('month', ao.time), 'Month')   as month,\
					EXTRACT(month from date_trunc('month', ao.time)) as monthval,\
					count(ao.delivery_id)                            as sale\
			from accounts_restaurant restaurant left join accounts_restaurantbranch branch\
					on restaurant.id = branch.restaurant_id\
					left join accounts_order ao on branch.id = ao.branch_id and ao.order_status = 'DELIVERED' and\
													date_part('year', ao.time) = date_part('year', CURRENT_DATE)\
			group by restaurant.restaurant_name, date_trunc('month', ao.time) \
			order by sale desc limit 3"
	branches_sales = namedtuplefetchall(query, [])

	fillcolors = ["rgba(220,0,220,0.3)", "rgba(0,220,220,0.3)", "rgba(220,90,220,0.3)", "rgba(120,220,220,0.3)"] * 3
	branches = {b.name: [0] * 12 for b in branches_sales}
	barcolors = {b.name: fillcolors.pop() for b in branches_sales}

	for b in branches_sales:
		if b.monthval is not None:
			branches[b.name][int(b.monthval) - 1] = b.sale

	return [{'name': b, 'sale': branches[b], 'fillColor': barcolors[b]} for b in branches.keys()]


def get_packagewise_order_completed_count_all(last_n_months=1):
	from browse.utils_db import namedtuplefetchall
	query = "select package.pkg_name as name, sum(order_pack.quantity) as sale\
			from browse_package package\
					join accounts_orderpackagelist order_pack on package.id = order_pack.package_id\
					join accounts_order ordr on order_pack.order_id = ordr.id\
			where ordr.order_status = 'DELIVERED'\
				and ordr.time >= CURRENT_DATE - INTERVAL '%s months'\
			group by package.pkg_name\
			order by sale desc"

	packages = namedtuplefetchall(query, [last_n_months])
	fillcolors = ["rgba(220,0,220,0.3)", "rgba(0,220,220,0.3)", "rgba(220,90,220,0.3)", "rgba(120,220,220,0.3)"] * len(
		packages)

	return [{'name': p.name, 'sale': p.sale, 'fillColor': fillcolors.pop()} for p in packages]
