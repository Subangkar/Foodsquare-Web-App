from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
# Create your views here.
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.base import View

from .forms import ProfileForm, UserForm
from accounts.account_links import *
from accounts.utils import *


def loginRender(request):
	return render(request, "accounts/login_v4.html")


def recoveryRender(request):
	return HttpResponse("Enter email to recover !!!")


def signupRender(request):
	return render(request, REGISTER_PAGE)


def homepageRender(request):
	return render(request, USER_DASHBOARD_PAGE)


def modalpageRender(request):
	return render(request, "index.html")


class ProfileView(TemplateView):
	template_name = 'accounts/profile.html'


class LoginView(TemplateView):
	template_name = 'accounts/login_v4.html'

	def get_context_data(self, **kwargs):
		if self.request.user.is_authenticated:
			print('Logged in: ' + str(self.request.user))
			# return redirect('/')

	def post(self, request, *args, **kwargs):
		print(pretty_request(request))
		username = request.POST.get('username', False)
		password = request.POST.get('pass', False)
		if username and password:
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('/')
			else:
				return HttpResponse('Error: User authentication error <a href="/login"">Try again</a>')
		else:
			return HttpResponse('Error: Username or password is empty <a href="/login">Try again</a>')


class RegisterView(TemplateView):
	template_name = 'accounts/colorlib-regform-7.html'

	def get_context_data(self, **kwargs):
		ctx = super(RegisterView, self).get_context_data(**kwargs)
		ctx['user_form'] = UserForm(prefix='user')
		# ctx['profile_form'] = ProfileForm(prefix='profile')
		return ctx

	def post(self, request, *args, **kwargs):
		print(request.POST)
		# print(pretty_request(request))

		username = request.POST.get('name', False)
		email = request.POST.get('email', False)
		password = request.POST.get('pass', False)
		password_confirm = request.POST.get('re_pass', False)

		# if password!=password_confirm
		# 	return

		user_form = UserForm(request.POST)
		# profile_form = ProfileForm(request.POST, request.FILES, prefix='profile')

		print(user_form)
		# print(profile_form)

		if user_form.is_valid():
			user = user_form.save(commit=False)
			# profile = profile_form.save(commit=False)
			user.save()
			# profile.user = user
			# profile.save()
			return HttpResponse("Signed Up!<br><a href='/'>Go to home</a>")
		else:
			return HttpResponse("Error : <a href='/signup'>Try again</a>!")


class LogoutView(View, LoginRequiredMixin):
	def get(self, request):
		logout(request)
		return redirect('/')

# class HomePageView(TemplateView):
