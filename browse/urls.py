from django.urls import path
from browse import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'browse'

urlpatterns = [
	path('', views.Index.as_view()),
	path('order/', views.Order.as_view()),
	# path('browse/item/', views.Item.as_view()),
	path('browse/restaurants/', views.RestaurantList.as_view()),
	# path('browse/', views.index),
	# path('submitOrder/', views.submitOrder),
	# path('allRestaurantList/', views.RestaurantList.as_view()),
	# path('menuEntryForRestaurant/', views.RestaurantMenuEntryList.as_view()),
	# path('branchListForRestaurant/', views.RestaurantBranchList.as_view())
	path('browse/raw/', views.viewRaw),

	path('browse/item/<int:id>/', views.PackageDetails.as_view(), name='Item'),
	path('browse/item/', views.PackageDetails.as_view(), name='Item'),
	# path('browse/item/<int:id>/', views.ItemDetailsRenderer, name='Item'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
