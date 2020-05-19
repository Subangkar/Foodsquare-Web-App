from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from browse import views

app_name = 'browse'

urlpatterns = [
	path('', views.Index.as_view(), name='home'),
	path('browse/', views.OrderView.as_view(), name='package-list'),
	path('offer/', views.OfferView, name='offer-list'),
	path('about/', views.aboutSection),
	path('contact/', views.contactSection),
	path('branch_pkg_availability/', views.branch_pkg_availability),
	path('browse/filter/', views.FilteredProducts, name='rating_filter'),

	path('browse/restaurants/', views.RestaurantList.as_view(), name='restaurants'),
	path('browse/branches/', views.RestaurantList.as_view(), name='branches'),

	# path('menuEntryForRestaurant/', views.RestaurantMenuEntryList.as_view()),
	# path('branchListForRestaurant/', views.RestaurantBranchList.as_view())
	path('browse/raw/', views.viewRaw),

	path('browse/item/<int:id>/', views.PackageDetails.as_view(), name='package-details'),
	path('browse/item/<int:id>/submitReview/', views.submitReview),
	path('browse/item/<int:id>/submitRating/', views.submitPackageRating),
	path('browse/item/<int:id>/reactOn/', views.reactSubmit),

	path('browse/restaurants/<int:id>/', views.RestaurantDetails.as_view(), name='restaurant_detail'),

	path('browse/branches/<int:id>/', views.RestaurantBranchDetails.as_view(), name='Branch_detail'),
	path('browse/branches/<int:id>/submitRating/', views.submitBranchRating),
	path('browse/branches/<int:id>/submitReview/', views.submitReview),
	path('browse/branches/<int:id>/reactOn/', views.reactSubmit),

	path('order/checkout/', views.CheckoutView.as_view(), name='checkout'),
	path('order/checkout/bkashPayment', views.bkashPayment, name='bkashPayment'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
