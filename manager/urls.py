from django.urls import path, include

from manager import views

app_name = 'manager'

urlpatterns = [

	path('', views.IndexView.as_view(), name='index'),
	path('homepage/', views.EditRestaurantView.as_view(), name='homepage'),
	path('orders/', views.ProcessOrdersView.as_view(), name='orders'),
	path('add_menu/', views.AddMenuView.as_view(), name='add_menu'),
	path('acceptOrder/', views.acceptOrder, name='1'),

	path('accounts/', include('accounts.urls'), name='accounts'),
	path('delivery_option/', views.DeliveryAvailability, name='delivery_option'),

]
