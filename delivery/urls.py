from django.urls import path, include

from delivery import views

app_name = 'delivery'

urlpatterns = [

	path('', views.IndexView.as_view(), name='index'),
	path('editProfile/', views.EditProfileView.as_view(), name='editProfile'),
	path('orders/', views.AcceptOrdersView.as_view(), name='orders'),
	path('applyForDelivery/', views.acceptDelivery, name='applyForDelivery'),

	path('accounts/', include('accounts.urls'), name='accounts'),

]

