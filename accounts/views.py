from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from django.views.generic import TemplateView
from django.views.generic.base import View

from accounts.account_links import *
from accounts.models import *
from accounts.utils import *
from .forms import UserForm, RestaurantBranchForm

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="foodsquare")


def recoveryRender(request):
	return HttpResponse("Enter email to recover !!!")


def homepageRender(request):
	return render(request, USER_DASHBOARD_PAGE)


class LoginView(TemplateView):
	template_name = 'accounts/login_v4.html'

	def get(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('/')
		else:
			return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		ctx = {'loggedIn': self.request.user.is_authenticated}
		return ctx

	def post(self, request, *args, **kwargs):
		print(pretty_request(request))
		username = request.POST.get('username', False)
		password = request.POST.get('pass', False)
		if username and password:
			user = authenticate(request, username=username, password=password)
			if user is not None and user.is_customer:
				login(request, user)
				print('Signing in: ' + str(request.user))
				return redirect('/')
			elif user is None:
				return render(request, 'accounts/message_page.html',
				              {'header': "Error !", 'details': 'Invalid Username or Password',
				               'redirect': reverse('accounts:login')})
			# return JsonResponse({'account': False})
			elif not user.is_customer:
				return render(request, 'accounts/message_page.html',
				              {'header': "Error !", 'details': 'Not a Customer account',
				               'redirect': reverse('accounts:login')})
		# return JsonResponse({'account': True, 'customer': False})
		else:
			return render(request, 'accounts/message_page.html',
			              {'header': "Error !", 'details': 'Username or password is empty',
			               'redirect': reverse('accounts:login')})


class ManagerLoginView(TemplateView):
	template_name = 'accounts/Manager_Login.html'

	def get(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('/homepage')
		else:
			return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		ctx = {'loggedIn': self.request.user.is_authenticated}
		return ctx

	def post(self, request, *args, **kwargs):
		print(pretty_request(request))
		username = request.POST.get('username', False)
		password = request.POST.get('pass', False)
		if username and password:
			user = authenticate(request, username=username, password=password)
			if user is None:
				return render(request, 'accounts/message_page.html',
				              {'header': "Error !", 'details': 'Invalid Username or Password',
				               'redirect': reverse('accounts:manger_login')})
			if user.is_branch_manager:
				login(request, user)
				print('Signing in: ' + str(request.user))
				return redirect('/orders')
			elif user.is_manager:
				rest = Restaurant.objects.get(user=user)
				if rest.restaurant_key.strip() != '0':
					login(request, user)
					print('Signing in: ' + str(request.user))
					return redirect('/homepage')
				elif rest.restaurant_key.strip() == '0':
					return render(request, 'accounts/message_page.html',
					              {'header': "Error !", 'details': 'Your account has not been approved yet'})
			elif not user.is_manager or not user.is_branch_manager:
				return render(request, 'accounts/message_page.html',
				              {'header': "Error !", 'details': 'Not a Manager or Branch Manager account',
				               'redirect': reverse('accounts:manger_login')})
			else:
				return render(request, 'accounts/message_page.html',
				              {'header': "Error !", 'details': 'User authentication error',
				               'redirect': reverse('accounts:manger_login')})
		else:
			return render(request, 'accounts/message_page.html',
			              {'header': "Error !", 'details': ' Username or password is empty',
			               'redirect': reverse('accounts:manger_login')})


class DeliveryLoginView(TemplateView):
	template_name = 'accounts/Delivery_Login.html'

	def get(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('/orders')
		else:
			return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		ctx = {'loggedIn': self.request.user.is_authenticated}
		return ctx

	def post(self, request, *args, **kwargs):
		print(pretty_request(request))
		username = request.POST.get('username', False)
		password = request.POST.get('pass', False)
		if username and password:
			user = authenticate(request, username=username, password=password)
			if user.is_delivery_man:
				if user is not None:
					login(request, user)
					print('Signing in: ' + str(request.user))
					return redirect('/orders')
				else:
					return render(request, 'accounts/message_page.html',
					              {'header': "Error !", 'details': '  User authentication error'})

		else:
			return render(request, 'accounts/message_page.html',
			              {'header': "Error !", 'details': ' Username or password is empty'})


class AdminLoginView(TemplateView):
	template_name = 'accounts/Manager_Login.html'

	def get(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('/homepage')
		else:
			return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		ctx = {'loggedIn': self.request.user.is_authenticated}
		return ctx

	def post(self, request, *args, **kwargs):
		print(pretty_request(request))
		username = request.POST.get('username', False)
		password = request.POST.get('pass', False)
		if username and password:
			user = authenticate(request, username=username, password=password)
			if user is not None and user.is_superuser:
				login(request, user)
				print('Signing in: ' + str(request.user))
				return redirect('/homepage')
			elif not user.is_superuser:
				return render(request, 'accounts/message_page.html',
				              {'header': "Error !", 'details': ' Not an admin account'})
			else:
				return render(request, 'accounts/message_page.html',
				              {'header': "Error !", 'details': '  User authentication error'})
		else:
			return render(request, 'accounts/message_page.html',
			              {'header': "Error !", 'details': ' Username or password is empty'})


class RegisterView(TemplateView):
	template_name = 'accounts/colorlib-regform-7.html'

	def get(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('/')
		else:
			return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		ctx = super(RegisterView, self).get_context_data(**kwargs)
		ctx['user_form'] = UserForm(prefix='user')
		# ctx['profile_form'] = ProfileForm(prefix='profile')
		ctx = {'loggedIn': self.request.user.is_authenticated}
		return ctx

	def post(self, request, *args, **kwargs):
		print(pretty_request(request))

		user_form = UserForm(request.POST)

		if user_form.is_valid():
			user = user_form.save(commit=False)
			user.is_customer = True
			user.save()
			p = UserProfile.objects.create(user=user)
			p.save()
			print('Registering : ' + str(request.user))
			login(request, user)
			return redirect('/')
		# return HttpResponse("Signed Up!<br><a href='/'>Go to home</a>")
		else:
			return render(request, 'accounts/message_page.html',
			              {'header': "Error !", 'details': ' signup'})


class ManagerRegisterView(TemplateView):
	template_name = 'accounts/Manager_Registration_form.html'

	def get(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('/')
		else:
			return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		ctx = super(ManagerRegisterView, self).get_context_data(**kwargs)
		ctx['user_form'] = UserForm(prefix='user')
		# ctx['profile_form'] = ProfileForm(prefix='profile')
		ctx = {'loggedIn': self.request.user.is_authenticated}
		return ctx

	def post(self, request, *args, **kwargs):
		print(pretty_request(request))

		if request.POST.get('password') != request.POST.get('re_pass'):
			return

		user_form = UserForm(request.POST)
		user = None
		if user_form.is_valid():
			user = user_form.save(commit=False)
			user.is_manager = True
			user.save()
			login(request, user)
		# UserProfile.objects.create(user=user).save() # lagbe na i guess
		else:
			return HttpResponse("Invalid Form or pass")

		rest = Restaurant()
		# rest.user = User(username=request.POST['username'], password=request.POST['password'],
		#                  email=request.POST['email'])
		rest.restaurant_name = request.POST['rest_name']
		rest.trade_license = request.POST['trade_license']

		# rest.user.save()
		# rest.user = User.objects.get(username=request.POST['username'])
		rest.user = user
		rest.save()
		return redirect('/homepage')


class DeliveryRegister(TemplateView):
	template_name = 'accounts/Delivery_Registration_Form.html'

	def get(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('/orders')
		else:
			return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		ctx = super(DeliveryRegister, self).get_context_data(**kwargs)
		ctx['user_form'] = UserForm(prefix='user')
		# ctx['profile_form'] = ProfileForm(prefix='profile')
		ctx = {'loggedIn': self.request.user.is_authenticated}
		ctx['locations'] = set([x.location_area for x in RestaurantBranch.objects.raw("select * from accounts_restaurantbranch \
		where location_area notnull and location_area!=\'\'")])
		return ctx

	def post(self, request, *args, **kwargs):
		print(pretty_request(request))

		if request.POST.get('password') != request.POST.get('re_pass'):
			return
		nid = request.POST.get('nid')
		contact = request.POST.get('contact')
		area = request.POST.get('area')
		user_form = UserForm(request.POST)
		print(user_form)
		if contact is None or area is None:
			contact = '01854478314'
			area = 'Khilgaon'
		user = None
		if user_form.is_valid():
			user = user_form.save(commit=False)
			user.is_delivery_man = True
			user.save()
			DeliveryMan(user=user, nid=nid, name=user.username, contactNum=contact, address=area).save()
			login(request, user)
		# UserProfile.objects.create(user=user).save() # lagbe na i guess
		else:
			return render(request, 'accounts/message_page.html',
			              {'header': "Error !", 'details': ' Invalid Form or pass'})

		return redirect('/orders')


class BranchRegisterView(TemplateView):
	template_name = 'accounts/Branch_Registration_Form.html'

	def get(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('/')
		else:
			return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		ctx = super(BranchRegisterView, self).get_context_data(**kwargs)
		ctx['user_form'] = UserForm(prefix='user')
		# ctx['profile_form'] = ProfileForm(prefix='profile')
		ctx = {'loggedIn': self.request.user.is_authenticated}
		return ctx

	def post(self, request, *args, **kwargs):
		print(pretty_request(request))

		if request.POST.get('password') != request.POST.get('re_pass'):
			return

		user_form = UserForm(request.POST)
		user = None
		branch = RestaurantBranch()
		try:
			print(request.POST['rest_key'])
			rest = Restaurant.objects.get(restaurant_key=request.POST['rest_key'])
			print(rest)
			if user_form.is_valid():
				branch.branch_location = request.POST['lat'] + ',' + request.POST['lon']
				try:
					branch.location_area = geolocator.reverse(branch.branch_location, language='en').raw['address'][
						'suburb']
				except Exception:
					try:
						branch.location_area = geolocator.reverse(branch.branch_location, language='en').raw['address'][
							'neighbourhood']
					except Exception:
						print("Location NOT Reversed")

				branch.branch_name = request.POST['branch_name']
				branch.restaurant = rest
				print(branch.branch_name)

				try:
					branch.branch_location_details = request.POST['extra_details']
				except Exception:
					pass
				# branch.location_area = ...

				user = user_form.save(commit=False)
				user.is_branch_manager = True
				user.save()
				branch.user = user

				branch.save()
				login(request, user)
			else:
				return render(request, 'accounts/message_page.html',
				              {'header': "Error !", 'details': ' Invalid Form or pass'})
		except Exception as e:
			return render(request, 'accounts/message_page.html',
			              {'header': "Error !", 'details': ' Not Valid secret key'})

		# rest.user = User(username=request.POST['username'], password=request.POST['password'],
		#                  email=request.POST['email'])
		print(branch)
		from browse.models import Package
		for package in Package.objects.filter(restaurant=branch.restaurant):
			from browse.models import PackageBranchDetails
			PackageBranchDetails.add_package_to_all_branches(package.restaurant, package)
		return redirect('/homepage')


class LogoutView(View, LoginRequiredMixin):
	def get(self, request):
		print('Signing out: ' + str(request.user))
		logout(request)
		return redirect('/')


class ManagerLogoutView(View, LoginRequiredMixin):
	def get(self, request):
		print('Signing out: ' + str(request.user))
		logout(request)
		return redirect('/')
