from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


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
