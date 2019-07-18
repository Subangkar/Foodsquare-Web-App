from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView, ListView

from accounts.models import Restaurant
from webAdmin.utils import uniqueKey


class RestaurantListView(ListView):
	template_name = 'webAdmin/restaurant_list.html'
	queryset = Restaurant.objects.all()
	context_object_name = 'restaurants'


# def get(self, request, *args, **kwargs):
# 	print(request.user.id)
# 	return super(self.__class__, self).get(request, *args, **kwargs)
#
# def get_context_data(self, *args, **kwargs):
# 	context = super(RestaurantListView, self).get_context_data(*args, **kwargs)
# 	context[]
# 	return context
#
# def post(self, request, *args, **kwargs):
# 	pass


def requestAccept(request, id):
	obj = Restaurant.objects.get(id=id)
	obj.restaurant_key = uniqueKey()
	obj.save()
	return redirect('/homepage/')
