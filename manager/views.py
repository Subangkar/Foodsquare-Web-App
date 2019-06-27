from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
# Create your views here.
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.contrib.auth.models import User

from accounts.forms import UserForm, ProfileForm, RestaurantForm
from accounts.models import Restaurant
from accounts.utils import pretty_request
from browse.models import Ingredient
from .forms import MenuForm


class IndexView(TemplateView):
    template_name = 'manager/index.html'

    def get_context_data(self, **kwargs):
        context = {'loggedIn': False}
        if self.request.user.is_authenticated:
            context['loggedIn'] = True
        return context

    def post(self, request, *args, **kwargs):
        pass


class EditRestaurantView(TemplateView):
    template_name = 'manager/edit_restaurant.html'

    def get(self, request, *args, **kwargs):
        return super(self.__class__, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(EditRestaurantView, self).get_context_data(*args, **kwargs)
        context['restaurant'] = User.objects.get(id=self.request.user.id).restaurant
        print(context)

        return context

    def post(self, request, *args, **kwargs):
        print(request)
        oldUser = User.objects.get(id=request.user.id)
        user_form = UserForm(request.POST, oldUser)
        profile = User.objects.get(id=self.request.user.id).restaurant
        profile.user = oldUser
        profile_form = RestaurantForm(
            request.POST or None, request.FILES or None, instance=profile)
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
        pass


class AddMenuView(TemplateView):
    template_name = 'manager/add_menu.html'

    def get(self, request, *args, **kwargs):
        return super(self.__class__, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(AddMenuView, self).get_context_data()
        context['ingredient_list'] = Ingredient.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        pass
