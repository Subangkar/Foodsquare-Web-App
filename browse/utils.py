from math import sin, atan2, sqrt, cos

from geopy.units import radians


def pretty_request(request):
	headers = ''
	for header, value in request.META.items():
		if not header.startswith('HTTP'):
			continue
		header = '-'.join([h.capitalize() for h in header[5:].lower().split('_')])
		headers += '{}: {}\n'.format(header, value)

	return (
		'{method} HTTP/1.1\n'
		'Content-Length: {content_length}\n'
		'Content-Type: {content_type}\n'
		'{headers}\n\n'
		'{body}'
	).format(
		method=request.method,
		content_length=request.META['CONTENT_LENGTH'],
		content_type=request.META['CONTENT_TYPE'],
		headers=headers,
		body=request.body,
	)


def distance(p1, p2):
	# approximate radius of earth in km
	R = 6373.0
	lat1 = radians(float(p1.split(',')[0]))
	lon1 = radians(float(p1.split(',')[1]))

	lat2 = radians(float(p2.split(',')[0]))
	lon2 = radians(float(p2.split(',')[1]))

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c
	# print(distance)
	return distance


# print(distance("52.2296756,21.0122287", "52.406374,16.9251681"))


# ------------------- Pagination --------------------
def get_page_objects(qset, page, items_per_page=0):
	"""
	https://docs.djangoproject.com/en/2.2/topics/pagination/
	:param qset: queryset or array
	:param page: page no to view
	:param items_per_page: no of items per page
	:return: page object which is iterable
	"""
	if page is None or page == 0:
		page = 1
	if items_per_page is None or items_per_page == 0:
		from webAdmin.utils import get_no_items_per_page
		items_per_page = get_no_items_per_page()
	from django.core.paginator import Paginator
	return Paginator(qset, items_per_page).get_page(page)
