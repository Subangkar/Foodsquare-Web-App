from django.urls import path

from . import views

app_name = 'customer'
urlpatterns = [
	path('editProfile/', views.EditProfileView.as_view()),
	path('myOrders/', views.myOrdersList.as_view(), name='homepage'),
	path('submitDeliveryRating/', views.submitDeliveryRating),
	path('get_notifications/', views.get_notifications),
	path('read_notifications/', views.read_notifcations),

]
