from django.urls import path
from browse import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'browse'

urlpatterns = [
	path('', views.Index.as_view(), name='home'),
	path('/', views.Order.as_view(), name='package-list'),

	path('browse/restaurants/', views.RestaurantList.as_view(), name='restaurants'),
	# path('menuEntryForRestaurant/', views.RestaurantMenuEntryList.as_view()),
	# path('branchListForRestaurant/', views.RestaurantBranchList.as_view())
	path('browse/raw/', views.viewRaw),

	path('browse/item/<int:id>/', views.PackageDetails.as_view(), name='package-details'),
	path('browse/restaurants/<int:id>/', views.RestaurantDetails.as_view(), name='restaurant_detail'),

	path('order/checkout/', views.checkoutView.as_view(), name='checkout'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
