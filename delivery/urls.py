from django.urls import path, include

from delivery import views

app_name = 'delivery'

urlpatterns = [

	path('', views.IndexView.as_view(), name='index'),
	path('editProfile/', views.EditProfileView.as_view(), name='editProfile'),
	path('orders/', views.AcceptOrdersView.as_view(), name='orders'),
	path('delivered_orders/', views.Delivered_Orders.as_view(), name='orders'),
	path('applyForDelivery/', views.acceptDelivery, name='applyForDelivery'),
	path('submitCustomerRating/', views.submitCustomerRating, name='submitCustomerRating'),
	path('delivery_info/', views.delivery_details),
	path('get_notifications/', views.get_notifications),
	path('read_notifications/', views.read_notifications),

	path('accounts/', include('accounts.urls'), name='accounts'),

]
