from django.urls import path, include

from manager import views

app_name = 'manager'

urlpatterns = [

	path('', views.IndexView.as_view(), name='index'),
	path('homepage/', views.EditRestaurantView.as_view(), name='homepage'),
	path('orders/', views.ProcessOrdersView.as_view(), name='orders'),
	path('add_menu/', views.AddMenuView.as_view(), name='add_menu'),
	path('view_menu/', views.ViewMenusView.as_view(), name='view_menus'),
	path('view_menu/<int:id>/', views.EditMenuView.as_view(), name='edit_menu'),

	path('acceptOrder/', views.acceptOrder, name='1'),

	path('accounts/', include('accounts.urls'), name='accounts'),
	path('delivery_option/', views.DeliveryAvailability, name='delivery_option'),

	# for branch manager
	path('edit_menu/<int:id>/', views.EditMenuView.as_view(), name='package-branch-details')

]
