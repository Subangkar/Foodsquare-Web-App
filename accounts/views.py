from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views.generic.base import View
from geopy.geocoders import Nominatim

from accounts.account_links import *
from accounts.models import *
from accounts.utils import *
from .forms import UserForm

geolocator = Nominatim(user_agent="foodsquare")

from django.core.mail import send_mail


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
			if user and user.is_delivery_man:
				login(request, user)
				print('Signing in: ' + str(request.user))
				return redirect('/orders')
			else:
				return render(request, 'accounts/message_page.html',
				              {'header': "Error !", 'details': '  User authentication error',
				               'redirect': reverse('accounts:delivery_login')})

		else:
			return render(request, 'accounts/message_page.html',
			              {'header': "Error !", 'details': ' Username or password is empty',
			               'redirect': reverse('accounts:delivery_login')})


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
			send_mail(
				'Account Activation Pending',
				'You have applied for creating a Restaurant Account.\n '
				'Username:' + user.username + '\n ' +
				'Email:' + user.email + '\n ' +
				'Password:' + request.POST.get('password') + '\n ' +
				'Restaurant:' + request.POST['rest_name'] + '\n ' +
				'Trade License:' + request.POST['trade_license'] + '\n ' +
				'We are verifying your information.\n ' +
				'You will be notified via this email when we are done.',
				'accounts@foodsquare',
				[user.email],
				fail_silently=False,
			)

			user.save()
			rest = Restaurant()
			rest.restaurant_name = request.POST['rest_name']
			rest.trade_license = request.POST['trade_license']

			rest.user = user
			rest.save()
			from webAdmin.utils import send_notification_to_admin
			send_notification_to_admin(rest.restaurant_name + "'s registration is pending for approval")
			return render(request, 'accounts/message_page.html',
			              {'header': "Registration Pending", 'details': 'Check your inbox (' + user.email + ')'})
		else:
			return render(request, 'accounts/message_page.html',
			              {'header': "Registration Failed!!!", 'details': 'Invalid Form Data'})


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
			return render(request, 'accounts/message_page.html', {'header': "Error !", 'details': ' Invalid Password'})

		# --------------------------------------------------
		user_form = UserForm(request.POST)
		if not user_form.is_valid():
			return render(request, 'accounts/message_page.html',
			              {'header': "Error !", 'details': ' Invalid Form or pass'})

		if not Restaurant.objects.filter(restaurant_key=request.POST['rest_key']).exists():
			return render(request, 'accounts/message_page.html',
			              {'header': "Error !", 'details': ' Not Valid secret key'})

		if request.POST['lat'] is None or request.POST['lon'] is None:
			return render(request, 'accounts/message_page.html',
			              {'header': "Error !", 'details': ' No Location Provided'})

		branch = RestaurantBranch()
		branch.branch_name = request.POST['branch_name']
		branch.restaurant = Restaurant.objects.get(restaurant_key=request.POST['rest_key'])
		branch.branch_location = request.POST['lat'] + ',' + request.POST['lon']
		if request.POST.get('extra_details') is not None:
			branch.branch_location_details = request.POST.get('extra_details')
		try:
			branch.location_area = geolocator.reverse(branch.branch_location, language='en').raw['address'][
				'suburb']
		except Exception:
			try:
				branch.location_area = geolocator.reverse(branch.branch_location, language='en').raw['address'][
					'neighbourhood']
			except Exception:
				print("Location NOT Reversed")
		user = user_form.save(commit=False)
		user.is_branch_manager = True
		user.save()
		branch.user = user

		branch.save()
		login(request, user)
		from customer.utils_db import send_notification
		send_notification(branch.restaurant.user.id, branch.branch_name + " was added under your restaurant")
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
