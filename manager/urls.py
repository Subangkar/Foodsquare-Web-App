from django.urls import path
from manager import views


app_name = 'manager'

urlpatterns = [

	path('', views.LoginView.as_view(), name='login'),

]

