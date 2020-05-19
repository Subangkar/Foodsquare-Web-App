from django.urls import path, include

from accounts import views

app_name = 'accounts'

urlpatterns = [
	path('login/', views.LoginView.as_view(), name='login'),

	path('manager_login/', views.ManagerLoginView.as_view(), name='manger_login'),
	path('delivery_login/', views.DeliveryLoginView.as_view(), name='delivery_login'),
	path('manager_register/', views.ManagerRegisterView.as_view(), name='manager_register'),
	path('delivery_register/', views.DeliveryRegister.as_view(), name='delivery_register'),
	path('branch_register/', views.BranchRegisterView.as_view(), name='branch_register'),

	path('admin_login/', views.AdminLoginView.as_view(), name='admin_login'),

	path('register/', views.RegisterView.as_view(), name='register'),
	path(r'register/facebook-signUp/', include('allauth.urls'), name='facebook-signUp'),

	path('recovery/', views.recoveryRender, name='recovery'),

	path('logout/', views.LogoutView.as_view(), name='logout'),
	path('manager_logout/', views.ManagerLogoutView.as_view(), name='manager_logout'),
	path('delivery_logout/', views.ManagerLogoutView.as_view(), name='delivery_logout'),

	path('admin_logout/', views.ManagerLogoutView.as_view(), name='admin_logout'),

]
