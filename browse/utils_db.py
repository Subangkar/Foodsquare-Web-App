from django.db import connection
from collections import namedtuple


def namedtuplefetchall(query, param_list):
	"""Return all rows from a cursor as a namedtuple"""
	with connection.cursor() as cursor:
		cursor.execute(query, param_list)
		desc = cursor.description
		nt_result = namedtuple('Result', [col[0] for col in desc])
		return [nt_result(*row) for row in cursor.fetchall()]


def get_rating_count_package(pkg_id):
	"""Returns a dictionary with key as rating-value and value as count"""
	results = namedtuplefetchall('select rating, count(distinct user_id)\
from browse_packagerating\
where package_id = %s\
group by rating', [pkg_id])

	return dict(zip([row.rating for row in results], [row.count for row in results]))


def get_rating_package(pkg_id):
	results = namedtuplefetchall('select avg(rating) as avg_rating\
		from browse_packagerating\
		where package_id = %s', [pkg_id])
	return results[0].avg_rating


def get_reviews_package(user_id, pkg_id):
	"""returns list of comments as tuple (package_id, user_id, rating, comment, time, nlikes, ndislikes)"""
	results = namedtuplefetchall('select comment.package_id,\
		comment.user_id,\
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
where comment.user_id = %s and comment.package_id = %s\
UNION\
DISTINCT\
select comment.package_id,\
		comment.user_id,\
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
where comment.user_id != %s and comment.package_id = %s\
order by time desc', [user_id, pkg_id, user_id, pkg_id])
	return results


def get_rating_restaurant(rest_id):
	return 5


def get_reviews_restaurant(rest_id):
	return ""
