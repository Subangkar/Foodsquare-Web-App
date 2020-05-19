# ------------------- Package, Offers for Branch -------------------------


def update_offer_branch(user, branch_package_id, offer_type, start_date, end_date, **kwargs):
	"""
	Update offer details for a package in branch

	call either
		update_offer_branch(user, branch_package_id, PackageBranchDetails.NONE, start_date, end_date) or

		update_offer_branch(user, branch_package_id, PackageBranchDetails.DISCOUNT, start_date, end_date, discount_val=val) or

		update_offer_branch(user, branch_package_id, PackageBranchDetails.BUY_N_GET_N, start_date, end_date, buy_n=val, get_n=val)

	:param user: request.user
	:param branch_package_id: branch's package details id, **NOT ACTUAL PACKAGE ID**
	:param offer_type: must in one of (PackageBranchDetails.NONE, PackageBranchDetails.DISCOUNT, PackageBranchDetails.BUY_N_GET_N)
	:param kwargs: pass (discount_val=val) if offer_type==PackageBranchDetails.DISCOUNT else (buy_n=val, get_n=val)
	:param start_date: offer start date
	:param end_date: offer end date
	:return: true if offer is updated false otherwise
	"""
	if user.is_authenticated and user.is_branch_manager:
		from browse.models import PackageBranchDetails
		pkg_details = PackageBranchDetails.objects.get(id=branch_package_id)
		if pkg_details is not None:
			if offer_type == PackageBranchDetails.DISCOUNT:
				discount_val = kwargs['discount_val']
				pkg_details.set_discount_offer(start_date, end_date, discount_val=discount_val)
				return True
			elif offer_type == PackageBranchDetails.BUY_N_GET_N:
				buy_n = kwargs['buy_n']
				get_n = kwargs['get_n']
				pkg_details.set_buy_get_offer(start_date, end_date, buy_n=buy_n, get_n=get_n)
				return True
			elif offer_type == PackageBranchDetails.NONE:
				pkg_details.clear_offer()
				return True
	return False


def set_package_availability_branch(user, branch_package_id, available_status):
	if user.is_authenticated and user.is_branch_manager:
		from browse.models import PackageBranchDetails
		pkg_details = PackageBranchDetails.objects.get(id=branch_package_id)
		if pkg_details is not None:
			pkg_details.available = available_status
			pkg_details.save()
			return pkg_details.available


def get_packages_list_branch(user):
	"""
	:return: list of packages under this branch manager
	"""
	if user.is_authenticated and user.is_branch_manager:
		from browse.models import PackageBranchDetails
		return PackageBranchDetails.objects.filter(branch=user.restaurantbranch)


def get_package_branch(user, branch_package_id):
	"""
	:return: package details for this branch
	"""
	if user.is_authenticated and user.is_branch_manager:
		from browse.models import PackageBranchDetails
		return PackageBranchDetails.objects.get(id=branch_package_id)


# ---------------------- Dashboard -----------------------------

def get_monthwise_order_completed_count_restaurant(rest_id):
	from browse.utils_db import namedtuplefetchall
	query = "select branch.branch_name                               as name,\
					to_char(date_trunc('month', ao.time), 'Month')   as month,\
					EXTRACT(month from date_trunc('month', ao.time)) as monthval,\
					count(ao.delivery_id)                            as sale\
			from accounts_restaurantbranch branch\
					left join accounts_order ao on branch.id = ao.branch_id and ao.order_status = 'DELIVERED' and\
													date_part('year', ao.time) = date_part('year', CURRENT_DATE)\
			where branch.restaurant_id = %s\
			group by branch.branch_name, date_trunc('month', ao.time)"
	branches_sales = namedtuplefetchall(query, [rest_id])

	fillcolors = ["rgba(220,0,220,0.3)", "rgba(0,220,220,0.3)", "rgba(220,90,220,0.3)", "rgba(120,220,220,0.3)"] * 3
	branches = {b.name: [0] * 12 for b in branches_sales}
	barcolors = {b.name: fillcolors.pop() for b in branches_sales}

	for b in branches_sales:
		if b.monthval is not None:
			branches[b.name][int(b.monthval) - 1] = b.sale

	return [{'name': b, 'sale': branches[b], 'fillColor': barcolors[b]} for b in branches.keys()]


def get_monthwise_order_completed_count_branch(branch_id):
	from browse.utils_db import namedtuplefetchall
	query = "select to_char(date_trunc('month', ao.time), 'Month')   as month,\
					EXTRACT(month from date_trunc('month', ao.time)) as monthval,\
					count(ao.delivery_id)                            as sale\
			from accounts_restaurantbranch branch\
					left join accounts_order ao on branch.id = ao.branch_id and ao.order_status = 'DELIVERED' and\
													date_part('year', ao.time) = date_part('year', CURRENT_DATE)\
			where branch.id = %s\
			group by date_trunc('month', ao.time)"
	month_sales = namedtuplefetchall(query, [branch_id])

	fillcolors = ["#396AB1",
				  "#DA7C30",
				  "#3E9651",
				  "#CC2529",
				  "#535154",
				  "#6B4C9A",
				  "#922428",
				  "#45FF88"] * 3
	sales = [0] * 12
	for m in month_sales:
		if m.monthval is not None:
			sales[int(m.monthval) - 1] = m.sale

	return {'sale': sales, 'fillColor': fillcolors}


def get_packagewise_order_completed_count_restaurant(rest_id, last_n_months=1):
	from browse.utils_db import namedtuplefetchall
	query = "select package.pkg_name as name, sum(order_pack.quantity) as sale\
			from browse_package package\
					join accounts_orderpackagelist order_pack on package.id = order_pack.package_id\
					join accounts_order ordr on order_pack.order_id = ordr.id\
			where ordr.order_status = 'DELIVERED'\
				and package.restaurant_id = %s\
				and ordr.time >= CURRENT_DATE - INTERVAL '%s months'\
			group by package.pkg_name\
			order by sale desc"

	packages = namedtuplefetchall(query, [rest_id, last_n_months])
	fillcolors = ["#FF6384",
				  "#63FF84",
				  "#84FF63",
				  "#8463FF",
				  "#6384FF",
				  "#44EF93",
				  "#5466FD",
				  "#2314EF"
				  ] * len(
		packages)

	return [{'name': p.name, 'sale': p.sale, 'fillColor': fillcolors.pop()} for p in packages]


def get_packagewise_order_completed_count_branch(branch_id, last_n_months=1):
	from browse.utils_db import namedtuplefetchall
	query = "select package.pkg_name as name, sum(order_pack.quantity) as sale\
			from browse_package package\
			         join browse_packagebranchdetails branch_pack on package.id = branch_pack.package_id\
			         join accounts_orderpackagelist order_pack on package.id = order_pack.package_id\
			         join accounts_order ordr on order_pack.order_id = ordr.id\
			where ordr.order_status = 'DELIVERED'\
			  and branch_pack.branch_id = %s\
			  and ordr.time >= CURRENT_DATE - INTERVAL '%s months'\
			group by package.pkg_name\
			order by sale desc"

	packages = namedtuplefetchall(query, [branch_id, last_n_months])
	fillcolors = ["#FF6384",
				  "#63FF84",
				  "#84FF63",
				  "#8463FF",
				  "#6581FE",
				  "#84FF63",
				  "#8D63FF",
				  "#6864FF"
				  ] * len(
		packages)

	return [{'name': p.name, 'sale': p.sale, 'fillColor': fillcolors.pop()} for p in packages]


def send_to_close_deliverymen(order):
	branch = order.branch
	from accounts.models import DeliveryMan
	deliverymen = DeliveryMan.objects.filter(address=branch.location_area, user__is_suspended=False)
	if deliverymen.exists():
		for deliveryman in deliverymen:
			from customer.utils_db import send_notification
			send_notification(deliveryman.user.id,
			                  "A new order with id: " + str(
				                  order.id) + " arrived for delivery from " + branch.branch_name)
