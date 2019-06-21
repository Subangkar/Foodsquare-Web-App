from django.urls import path, include

import accounts.views
from manager import views


app_name = 'manager'

urlpatterns = [

	path('', views.IndexView.as_view(), name='index'),
	path('homepage/', views.HomepageView.as_view(), name='homepage'),
	path('accounts/', include('accounts.urls'), name='accounts'),
]

