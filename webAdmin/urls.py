from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from webAdmin import views

app_name = 'webAdmin'

urlpatterns = [

	# path('', views.IndexView.as_view(), name='index'),
	path('homepage/', views.RestaurantListView.as_view(), name='restaruantList'),
	path('restaurant_info/', views.restaurantDetails),
	path('delivery_info/', views.DeliveyListView.as_view()),
	path('dashboard/', views.AdminDashBoardView.as_view()),
	path('branch_info/', views.branch_list),
	path('blocked_user/', views.BlockedUsersView.as_view()),
	path('blocked_delieryman/', views.BlockedDeliveryMenView.as_view()),
	path('editConfiguration/', views.EditConfigView.as_view()),

	path('', RedirectView.as_view(url='/accounts/admin_login'), name='accounts'),
	path('accounts/', include('accounts.urls'), name='accounts'),
	path('accept/<int:id>/', views.requestAccept),
	path('database/', admin.site.urls, name='dbadmin'),

	path('get_notifications/', views.get_notifications),
	path('read_notifications/', views.read_notifications),
	path('unblock/', views.unblock)

]
