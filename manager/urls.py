from django.urls import path, include

import accounts.views
from manager import views


app_name = 'manager'

urlpatterns = [

	path('', views.IndexView.as_view(), name='index'),
	path('homepage/', views.EditRestaurantView.as_view(), name='homepage'),
	path('add_menu/', views.AddMenuView.as_view(), name='add_menu'),

	path('accounts/', include('accounts.urls'), name='accounts'),
]

