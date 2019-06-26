from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.http import HttpResponse
# Create your views here.
from django.views.generic import TemplateView

from accounts.forms import UserForm, ProfileForm
from accounts.utils import pretty_request


class EditProfileView(TemplateView):
	template_name = 'customer/EditProfile.html'

	def get(self, request, *args, **kwargs):
		print(request.user.id)
		ob = User.objects.all()
		print(ob)
		# ob2 = UserProfile.objects.filter(user = request.user.id)
		# ob2 = User.objects.get(username='masum32145').userprofile
		# ob2.address = 'Paltan'
		# ob2.save()
		# print(ob2)
		# ob3 = User.objects.get(username='masum32145').userprofile
		# # ob2.address = "new market"
		# # ob2.save()
		# print(ob3)
		return super(self.__class__, self).get(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(EditProfileView, self).get_context_data(*args, **kwargs)
		print(pretty_request(self.request))
		try:
			obj = dict()
			obj['userprofile'] = User.objects.get(id=self.request.user.id).userprofile
			print(obj)
			obj['socialacnt'] = False
			context['userprofile'] = obj

		except Exception as e:
			obj = dict()
			obj = SocialAccount.objects.get(user_id=self.request.user.id).extra_data
			print(obj)
			obj['socialacnt'] = True
			try:  # for facebook
				obj['avatar'] = obj['picture']
				del obj['picture']
			except Exception as e1:
				pass
			context['userprofile'] = obj
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
