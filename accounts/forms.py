from django import forms
from django.contrib.auth.models import User
from django.forms.models import ModelForm

from .models import UserProfile, Restaurant, RestaurantBranch


class ProfileForm(ModelForm):

	class Meta:
		model = UserProfile
		fields = ( 'avatar','address')


class UserForm(ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username', 'password', 'email')
		# fields = ('name', 'email', 'pass', 're_pass', 'signup')

	def save(self, commit=True):
		new_user = User.objects.create_user(self.cleaned_data['username'],
		                                    self.cleaned_data['email'],
		                                    self.cleaned_data['password'])
		# new_user.first_name = self.cleaned_data['first_name']
		# new_user.last_name = self.cleaned_data['last_name']
		if commit:
			new_user.save()
		return new_user


# class RestaurantProfileForm(ModelForm):
#
# 	class Meta:
# 		model = Restaurant
# 		fields = ('restaurant_key', 'trade_license')
#
#
# class RestaurantBranchProfileForm(ModelForm):
#
# 	class Meta:
# 		model = RestaurantBranch
# 		fields = ('restaurant_key', 'trade_license')

