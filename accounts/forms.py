from django import forms
from django.forms.models import ModelForm

from accounts.models import User
from .models import UserProfile, Restaurant, RestaurantBranch


class ProfileForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = ('first_name', 'last_name', 'avatar', 'address')


class UserForm(ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username', 'password', 'email')

	def save(self, commit=True):
		new_user = User.objects.create_user(username=self.cleaned_data['username'],
		                                    email=self.cleaned_data['email'],
		                                    password=self.cleaned_data['password'])
		try:
			new_user.first_name = self.cleaned_data['first_name']
			new_user.last_name = self.cleaned_data['last_name']
		except Exception:
			pass
		if commit:
			new_user.save()
		return new_user


class RestaurantForm(ModelForm):
	class Meta:
		model = Restaurant
		fields = ('restaurantImg',)


class RestaurantBranchForm(ModelForm):
	class Meta:
		model = RestaurantBranch
		fields = ('branch_name', 'branch_location', 'branch_location_details',)

	def save(self, commit=True):
		location = ''
		print('vai ksu hoy na')
		print(self.cleaned_data)
		print(self.cleaned_data['lat'])
		print(+ ',' + self.cleaned_data['lon'])
		print(location)
		new_branch = RestaurantBranch.objects.create(branch_name=self.cleaned_data['branchName'],
		                                             branch_location=location)
		print(new_branch)
		try:
			new_branch.branch_location_details = self.cleaned_data['extra_details']
		except Exception:
			pass
		if commit:
			new_branch.save()
		return new_branch
# branch location field
