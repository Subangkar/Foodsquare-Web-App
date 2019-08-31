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


# ---------------- Offers to users --------------------------------------

def add_offer_to_customer(user, customer_id, start_date, end_date, discount, count):
	from accounts.models import User
	from browse.models import UserOffer
	customer = User.objects.get(id=customer_id)
	if user.is_authenticated and user.is_branch_manager and customer and customer.is_customer:
		UserOffer.add_offer(user.restaurantbranch.id, customer_id, start_date, end_date, discount, count)


def get_running_offers(user):
	"""
	:return: list of currently active offers of this branch
	"""
	if user.is_authenticated and user.is_branch_manager:
		from browse.models import UserOffer
		return UserOffer.running_offers(branch_id=user.restaurantbranch.id)


def get_offers_to_customer(user, customer_id):
	"""
	:return: list of currently active offers to the customer on this branch
	"""
	if user.is_authenticated and user.is_branch_manager:
		from browse.models import UserOffer
		return UserOffer.running_offers_to_customer(branch_id=user.restaurantbranch.id, customer_id=customer_id)
