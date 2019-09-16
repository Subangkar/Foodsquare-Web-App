from allauth.socialaccount.models import SocialAccount
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, ListView

from accounts.forms import UserForm, ProfileForm
from accounts.models import User, Order
from accounts.utils import pretty_request


class EditProfileView(TemplateView):
	template_name = 'customer/EditProfile.html'

	def get(self, request, *args, **kwargs):

		return super(self.__class__, self).get(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(EditProfileView, self).get_context_data(**kwargs)
		print(pretty_request(self.request))
		try:
			obj = dict()
			context['userprofile'] = User.objects.get(id=self.request.user.id).userprofile
			context['socialacnt'] = False

		except Exception as e:
			obj = dict()
			obj = SocialAccount.objects.get(user_id=self.request.user.id).extra_data
			context['socialacnt'] = True
			try:  # for facebook
				obj['avatar'] = obj['picture']
				del obj['picture']
			except Exception as e1:
				pass
			context['userprofile'] = obj
			print(context)
		return context

	def post(self, request, *args, **kwargs):
		print(request)
		oldUser = User.objects.get(id=request.user.id)
		user_form = UserForm(request.POST, oldUser)
		profile = oldUser.userprofile
		profile.user = oldUser
		profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
		print(profile_form)
		if profile_form.is_valid():
			profile_form.save()
			print('Registering : ' + str(request.user))
			return render(request, 'accounts/message_page.html',
						  {'header': "Signed Up!", 'details': '',
						   'redirect': reverse('customer:homepage')})

		else:
			return render(request, 'accounts/message_page.html',
						  {'header': "Error!", 'details': 'Try Again',
						   'redirect': reverse('customer:homepage')})
		pass


class myOrdersList(ListView):
	template_name = 'customer/trackOrder.html'
	context_object_name = 'Orders'

	def get_queryset(self):
		return Order.objects.filter(user=self.request.user)


def get_notifications(request):
	from customer.utils_db import get_unread_notifications
	unreads = get_unread_notifications(request.user)
	if unreads is not None:
		notifications = [notf.message for notf in unreads]
	else:
		notifications = []
	return JsonResponse({'notifications': notifications})


def read_notifcations(request):
	from datetime import datetime
	from customer.utils_db import read_all_notifications
	read_all_notifications(request.user, datetime.now())
	return JsonResponse({'Success': True})


def submitDeliveryRating(request):
	order_id = request.POST.get('order-id')
	rating = request.POST.get('rating')
	print(order_id)
	print(rating)
	from browse.utils_db import post_delivery_rating
	return JsonResponse({'success': post_delivery_rating(order_id, rating)})
