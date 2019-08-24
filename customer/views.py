from allauth.socialaccount.models import SocialAccount
from django.shortcuts import render

from accounts.models import User, Order
from django.http import HttpResponse
# Create your views here.
from django.views.generic import TemplateView, ListView

from accounts.forms import UserForm, ProfileForm
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
			return HttpResponse("Signed Up!<br><a href='/'>Go to home</a>")
		# if user_form.is_valid():
		# user = user_form.save(commit=False)
		# user.save()

		else:
			return HttpResponse("Error : <a href='/signup'>Try again</a>!")
		# menuForm = MenuForm(request.POST or None, request.FILES or None)
		# menuForm.save()
		# print(menuForm)
		# return HttpResponse("<h1>Congrats</h1>")
		pass


class myOrdersList(ListView):
	template_name = 'customer/trackOrder.html'
	queryset = Order.objects.all()
	context_object_name = 'Orders'


def get_notifications(request):
	from customer.utils_db import get_new_notifications, get_unread_notifications
	notifications = get_new_notifications(request.user)
	# notifications = get_unread_notifications(request.user)
	return render(request, 'customer/notifications.html', {'notifications': notifications, 'cnt': len(notifications)})
