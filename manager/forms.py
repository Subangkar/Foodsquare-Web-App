from django import forms
from django.contrib.auth.models import User
from django.forms.models import ModelForm

from manager.models import Menu


class MenuForm(ModelForm):
	class Meta:
		model = Menu
		fields = ('menu_name', 'price', 'menu_img')

