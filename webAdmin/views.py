from django.core import serializers
import json

from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView, ListView

from accounts.models import Restaurant
from webAdmin.utils import uniqueKey, get_deliverymen_list


class RestaurantListView(ListView):
	template_name = 'webAdmin/restaurant_list.html'
	queryset = Restaurant.objects.all()
	context_object_name = 'restaurants'


def requestAccept(request, id):
	obj = Restaurant.objects.get(id=id)
	obj.restaurant_key = uniqueKey()
	user = obj.user
	send_mail(
		'Account Activated',
		'You Restaurant Account has been activated.<br>' +
		'Username:' + user.username + '<br>' +
		'Restaurant:' + obj.restaurant_name + '<br>' +
		'Your Key:' + obj.restaurant_key + '<br>' +
		'You can now login with your username and password at.',
		'accounts@foodsquare',
		[obj.user.email],
		fail_silently=False,
	)
	obj.save()
	return redirect('/homepage/')


def restaurantDetails(request):
	id = request.GET.get('id')
	obj = Restaurant.objects.get(id=id)
	ser = serializers.serialize('json', [obj])
	json_obj = json.loads((ser.strip('[]')))
	print(json_obj['fields'])
	return JsonResponse(json_obj['fields'])


class DeliveyListView(ListView):
	template_name = 'webAdmin/delivery_info.html'
	queryset = get_deliverymen_list()
	context_object_name = 'delivery_men'
