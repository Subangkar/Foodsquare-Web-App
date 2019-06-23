from django.urls import path, include
from django.views.generic import RedirectView

import accounts.views
from webAdmin import views

app_name = 'webAdmin'

urlpatterns = [

	# path('', views.IndexView.as_view(), name='index'),
	path('homepage/', views.RestaurantListView.as_view(), name='restaruantList'),
	path('', RedirectView.as_view(url='/accounts/admin_login'), name='accounts'),
	path('accounts/', include('accounts.urls'), name='accounts'),
	path('accept/<int:id>/', views.requestAccept),

]