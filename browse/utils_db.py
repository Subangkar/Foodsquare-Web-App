from collections import namedtuple

from django.db import connection


# ------------------ util functions --------------------------


def namedtuplefetchall(query, param_list):
	"""Return all rows from a cursor as a namedtuple"""
	with connection.cursor() as cursor:
		cursor.execute(query, param_list)
		desc = cursor.description
		nt_result = namedtuple('Result', [col[0] for col in desc])
		return [nt_result(*row) for row in cursor.fetchall()]


# ------------------------ Restaurant / Branches -----------------------
class RestBranch:
	branch = None
	is_branch = False
	user = None
	restaurant_name = None
	restaurant_key = None
	trade_license = None
	restaurantImg = None
	id = None

	def __init__(self, restaurant, branch=None):
		self.user = restaurant.user
		self.restaurant_name = restaurant.restaurant_name
		self.restaurant_key = restaurant.restaurant_key
		self.trade_license = restaurant.trade_license
		self.restaurantImg = restaurant.get_image()
		self.get_image = restaurant.get_image()
		self.id = restaurant.id
		self.pk = restaurant.pk
		self.get_absolute_url = restaurant.get_absolute_url()

		if branch is not None:
			self.is_branch = True
			self.is_open_now = branch.is_open_now()
			# print(branch.get_absolute_url())
			self.get_absolute_url = branch.get_absolute_url()
			self.get_image = branch.get_image()

		self.addBranch(branch=branch)

	def __eq__(self, other):
		return self.branch == other.branch if self.branch else self.id == other.id

	def addBranch(self, branch):
		self.branch = branch
		self.is_branch = self.branch is not None


def branchesInRadius(coord, queryset):
	import functools
	from accounts.models import RestaurantBranch
	rest_map = {}
	rest_list = []
	for r in queryset:
		if r.restaurant.id in rest_map:
			rest_map[r.restaurant.id].append(r)
		else:
			rest_map[r.restaurant.id] = [r]
	for rest in rest_map.values():
		branches = sorted(rest, key=functools.cmp_to_key(lambda x, y: x.distance(coord) - y.distance(coord)))
		if branches[0].distance(coord) < RestaurantBranch.MAX_DELIVERABLE_DISTANCE:
			def_branch = branches[0]
			for branch in branches:
				if branch.is_open_now():
					def_branch = branch
					break
			rest_list.append(RestBranch(def_branch.restaurant, branch=def_branch))
	return rest_list


# ------------------- Review Ratings -------------------------


def get_rating_count_package(pkg_id):
	""":returns an array with index as rating-value and value as count"""
	results = namedtuplefetchall(
		'select rating, count(distinct user_id)\
		from browse_packagerating\
		where package_id = %s\
		group by rating', [pkg_id])
	ratings = [0, 0, 0, 0, 0, 0]
	for i in results:
		ratings[i.rating] = i.count
	return ratings


def get_rating_package(pkg_id):
	""":returns average rating of package"""
	results = namedtuplefetchall(
		'select avg(rating) as avg_rating\
		from browse_packagerating\
		where package_id = %s', [pkg_id])
	return results[0].avg_rating


def get_reviews_package(user_id, pkg_id):
	"""returns list of comments as tuple (package_id, comment_id, user_name, user_id, rating, comment, time, nlikes, ndislikes)
	with current user @ top """
	results = namedtuplefetchall(
		'select comment.package_id,\
			comment.id                       as comment_id,\
			account.username                 as user_name,\
			account.id                       as user_id,\
			rate.rating,\
			comment.comment,\
			comment.time,\
			(select count(liked.user_id)\
			from browse_packagecommentreact liked\
			where liked.post_id = comment.id\
				and liked.liked = true)		 as nlikes,\
			(select count(disliked.user_id)\
			from browse_packagecommentreact disliked\
			where disliked.post_id = comment.id\
				and disliked.disliked = true) as ndislikes\
		from browse_packagecomment comment\
				left join browse_packagerating rate on rate.package_id = comment.package_id and\
													rate.user_id = comment.user_id\
				join accounts_user account on comment.user_id = account.id\
		where comment.user_id = %s and comment.package_id = %s\
		UNION\
		DISTINCT\
		select *\
		from (\
			select comment.package_id,\
				comment.id                       as comment_id,\
				account.username                 as user_name,\
				account.id                       as user_id,\
				rate.rating,\
				comment.comment,\
				comment.time,\
				(select count(liked.user_id)\
				from browse_packagecommentreact liked\
				where liked.post_id = comment.id\
					and liked.liked = true)		 as nlikes,\
				(select count(disliked.user_id)\
				from browse_packagecommentreact disliked\
				where disliked.post_id = comment.id\
					and disliked.disliked = true) as ndislikes\
			from browse_packagecomment comment\
					left join browse_packagerating rate on rate.package_id = comment.package_id and\
														rate.user_id = comment.user_id\
					join accounts_user account on comment.user_id = account.id\
			where comment.user_id != %s and comment.package_id = %s\
			order by time desc\
		) other_comments', [user_id, pkg_id, user_id, pkg_id])
	return results


def get_react_count_package(post):
	""":returns (likes_count, dislikes_count) of post in package"""
	from browse.models import PackageCommentReact
	nliked = PackageCommentReact.objects.filter(post=post, liked=True).count()
	ndisliked = PackageCommentReact.objects.filter(post=post, disliked=True).count()
	return nliked, ndisliked


def get_rating_restaurant(rest_id):
	""":returns avg rating over all users from all branches"""
	results = namedtuplefetchall(
		'select avg(rating) as avg_rating\
		from browse_branchrating join accounts_restaurantbranch\
									on browse_branchrating.branch_id = accounts_restaurantbranch.id\
		where accounts_restaurantbranch.restaurant_id = %s', [rest_id])
	return results[0].avg_rating


def get_rating_branch(branch_id):
	""":returns avg rating over all users branch"""
	results = namedtuplefetchall(
		'select avg(rating) as avg_rating\
		from browse_branchrating join accounts_restaurantbranch\
									on browse_branchrating.branch_id = accounts_restaurantbranch.id\
		where accounts_restaurantbranch.restaurant_id = %s', [branch_id])
	return results[0].avg_rating


def get_reviews_branch(user_id, branch_id):
	"""returns list of comments as tuple (branch_id, comment_id, user_name, user_id, rating, comment, time, nlikes, ndislikes)
	with current user @ top """
	results = namedtuplefetchall(
		'select comment.branch_id,\
			comment.id                       as comment_id,\
			account.username                 as user_name,\
			account.id                       as user_id,\
			rate.rating,\
			comment.comment,\
			comment.time,\
			(select count(liked.user_id)\
			from browse_branchcommentreact liked\
			where liked.post_id = comment.id\
				and liked.liked = true)       as nlikes,\
			(select count(disliked.user_id)\
		from browse_branchcommentreact disliked\
		where disliked.post_id = comment.id\
			and disliked.disliked = true) as ndislikes\
		from browse_branchcomment comment\
				left join browse_branchrating rate on rate.branch_id = comment.branch_id and\
														rate.user_id = comment.user_id\
				join accounts_user account on comment.user_id = account.id\
		where comment.user_id = %s\
			and comment.branch_id = %s\
		UNION\
		DISTINCT\
		select *\
		from (\
			select comment.branch_id,\
				comment.id                       as comment_id,\
				account.username                 as user_name,\
				account.id                       as user_id,\
				rate.rating,\
				comment.comment,\
				comment.time,\
				(select count(liked.user_id)\
				from browse_branchcommentreact liked\
				where liked.post_id = comment.id\
					and liked.liked = true)       as nlikes,\
				(select count(disliked.user_id)\
				from browse_branchcommentreact disliked\
				where disliked.post_id = comment.id\
					and disliked.disliked = true) as ndislikes\
			from browse_branchcomment comment\
					left join browse_branchrating rate on rate.branch_id = comment.branch_id and\
															rate.user_id = comment.user_id\
					join accounts_user account on comment.user_id = account.id\
			where comment.user_id != %s\
				and comment.branch_id = %s\
			order by time desc\
		) other_comments', [user_id, branch_id, user_id, branch_id])
	return results


def get_react_count_branch(post):
	""":returns (likes_count, dislikes_count) of post in branch"""
	from browse.models import BranchCommentReact
	nliked = BranchCommentReact.objects.filter(post=post, liked=True).count()
	ndisliked = BranchCommentReact.objects.filter(post=post, disliked=True).count()
	return nliked, ndisliked


def post_rating_package(user, pkg_id, rating):
	""" create or update user rating on package """
	from browse.models import PackageRating
	from browse.models import Package
	package = Package.objects.get(id=pkg_id)
	post, _ = PackageRating.objects.get_or_create(package=package, user=user)
	post.rating = rating
	post.save()


def post_comment_package(user, pkg_id, comment):
	""" create or update user comment on package """
	from browse.models import PackageComment
	from browse.models import Package
	package = Package.objects.get(id=pkg_id)
	post, _ = PackageComment.objects.get_or_create(package=package, user=user)
	post.comment = comment
	post.save()


def post_comment_react_package(user, comment_id, react_val):
	"""
	create or update react on existing post of any user on package
	:returns updated (likes_count, dislikes_count) of that post
	"""
	from browse.models import PackageComment, PackageCommentReact
	post = PackageComment.objects.get(id=comment_id)
	if react_val in ['like', 'dislike']:
		react, _ = PackageCommentReact.objects.get_or_create(post=post, user=user)
		print(react)

		react.liked = (react_val == 'like')
		react.disliked = (react_val == 'dislike')
		react.save()
	return get_react_count_package(post)


def post_rating_branch(user, branch_id, rating):
	""" create or update user rating on branch """
	from browse.models import BranchRating
	from accounts.models import RestaurantBranch
	branch = RestaurantBranch.objects.get(id=branch_id)
	post, _ = BranchRating.objects.get_or_create(branch=branch, user=user)
	post.rating = rating
	post.save()


def post_comment_branch(user, branch_id, comment):
	""" create or update user comment on branch """
	from browse.models import BranchComment
	from accounts.models import RestaurantBranch
	branch = RestaurantBranch.objects.get(id=branch_id)
	post, _ = BranchComment.objects.get_or_create(branch=branch, user=user)
	post.comment = comment
	post.save()


def post_comment_react_branch(user, comment_id, react_val):
	"""
	create or update react on existing post of any user on branch
	:returns updated (likes_count, dislikes_count) of that post
	"""
	from browse.models import BranchComment, BranchCommentReact
	post = BranchComment.objects.get(id=comment_id)
	if react_val in ['like', 'dislike']:
		react, _ = BranchCommentReact.objects.get_or_create(post=post, user=user)
		react.liked = (react_val == 'like')
		react.disliked = (react_val == 'dislike')
		react.save()
	return get_react_count_branch(post)


# ------------ Packages -----------------------------

def get_named_package(name):
	"""
	:param name: package-name / restaurant-name / category-name / ingredient-name
	:return: set of packages satisfying above criteria
	"""
	from browse.models import Package
	return (Package.objects.filter(
		pkg_name__icontains=name) | Package.objects.filter(
		# restaurant__restaurant_name__icontains=name) | Package.objects.filter(
		ingr_list__name__icontains=name) | Package.objects.filter(
		category__icontains=name)).distinct()


def get_rated_package(rating=0):
	from browse.models import PackageRating
	from django.db.models import Avg
	pkg_ids = PackageRating.objects.values('package').annotate(avg=Avg('rating')).filter(
		avg__gte=rating).values('package').distinct()
	from browse.models import Package
	return Package.objects.filter(id__in=pkg_ids).distinct()


def get_price_range_package(low=0.0, high=90000.0):
	from browse.models import Package
	from django.db.models import Q
	return Package.objects.filter(Q(price__gte=low) & Q(price__lte=high)).distinct()


def get_category_packages(categoty_name):
	"""
	:param categoty_name: category-name
	:return: set of packages satisfying above criteria
	"""
	from browse.models import Package
	return Package.objects.filter(category__iexact=categoty_name).distinct()


# ----------- Branch/Restaurant Packages ----------------------

def get_available_packages_branch(branch_id):
	"""
	:return: list PackageBranchDetails of packages currently available in this branch
	"""
	from browse.models import PackageBranchDetails
	packages = PackageBranchDetails.objects.filter(branch_id=branch_id)
	return filter(lambda x: x.is_available(), packages)


def get_available_offer_packages_branch(branch_id):
	"""
	:return: list PackageBranchDetails of packages with offer in this branch
	"""
	from browse.models import PackageBranchDetails
	packages = PackageBranchDetails.objects.filter(branch_id=branch_id)
	return filter(lambda x: x.has_any_offer(), packages)


def get_searched_packages_branch(branch_id, search_key):
	"""
	:return: list PackageBranchDetails of available packages satisfying provided parameter in this branch
	"""
	from browse.models import PackageBranchDetails
	from django.db.models import Q
	packages = PackageBranchDetails.objects.filter(Q(branch_id=branch_id) &
	                                               (Q(package__pkg_name__icontains=search_key) |
	                                                Q(package__category__icontains=search_key) |
	                                                Q(package__ingr_list__name__icontains=search_key))).distinct()
	return filter(lambda pkg: pkg.is_available(), packages)


def get_available_packages_restaurant(rest_id):
	"""
	:return: list PackageBranchDetails of packages currently available in any branch of provided restaurant
	"""
	from browse.models import PackageBranchDetails
	packages = PackageBranchDetails.objects.filter(branch__restaurant__id=rest_id)
	return filter(lambda x: x.package.is_available_in_any_branch(), packages)


def get_searched_packages_restaurant(rest_id, search_key):
	"""
	:return: list PackageBranchDetails of available packages in any branch of provided restaurant satisfying provided parameter
	"""
	from browse.models import PackageBranchDetails
	from django.db.models import Q
	packages = PackageBranchDetails.objects.filter(Q(branch__restaurant__id=rest_id) &
	                                               (Q(package__pkg_name__icontains=search_key) |
	                                                Q(package__category__icontains=search_key) |
	                                                Q(package__ingr_list__name__icontains=search_key))).distinct()
	return filter(lambda pkg: pkg.package.is_available_in_any_branch(), packages)


def get_price_for_branch_pkg(branchPack_id, quantity):
	from browse.models import PackageBranchDetails
	return PackageBranchDetails.objects.get(id=branchPack_id).get_buying_price(order_quantity=quantity)


# ------------------------ Offers ------------------------------

def get_deliverable_offers(package_id, coordinates):
	"""
	:param package_id: restaurant's package_id
	:param coordinates: "x,y" format
	:return: list of PackageOfferDetail(branch_package=branch_pack, deliverable=True/False)
	"""
	from browse.models import Package
	try:
		from browse.models import PackageBranchDetails
		branch_detail_list = PackageBranchDetails.objects.filter(package__id=package_id)
		import collections
		PackageOfferDetail = collections.namedtuple('PackageOfferDetail',
		                                            ['branch_package', 'deliverable', 'branch_url'])
		return [PackageOfferDetail(branch_package=pkg, deliverable=pkg.is_deliverable_to(coordinates),
		                           branch_url=pkg.branch.get_absolute_url())
		        for pkg in branch_detail_list]
	except Package.DoesNotExist:
		return []


# ------------------------ Delivery ----------------------------

def post_delivery_rating(order_id, rating):
	from accounts.models import Order
	try:
		order = Order.objects.get(id=order_id)
		print(order_id)
		order.delivery.rating_deliveryman = int(rating)
		order.delivery.save()
		return True
	except Order.DoesNotExist:
		return False


#  ----------------------- Insert utils -------------------------
def insert_package(pkg_name, inglist, price, for_n_persons, category, restaurant_id):
	from browse.models import Package
	from accounts.models import Restaurant
	restaurant = Restaurant.objects.get(id=restaurant_id)
	package, _ = Package.objects.get_or_create(pkg_name=pkg_name, category=category, price=price,
	                                           for_n_persons=for_n_persons,
	                                           restaurant=restaurant)
	for ingr in inglist:
		from browse.models import Ingredient
		from browse.models import IngredientList
		ingr = str(ingr).strip().lower()
		ingredient, _ = Ingredient.objects.get_or_create(name=ingr)
		IngredientList.objects.get_or_create(package=package, ingredient=ingredient)

	from browse.models import PackageBranchDetails
	PackageBranchDetails.add_package_to_all_branches(package.restaurant, package)
