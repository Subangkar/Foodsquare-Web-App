from django.conf.urls import url
from django.urls import path, include
from accounts import views

# from .views import (
#     LoginView, ResendActivationCodeView, RemindUsernameView, SignUpView, ActivateView, LogOutView,
#     ChangeEmailView, ChangeEmailActivateView, ChangeProfileView, ChangePasswordView,
#     RestorePasswordView, RestorePasswordDoneView, RestorePasswordConfirmView,
# )

app_name = 'accounts'

urlpatterns = [
	# path('', views.loginRender, name='home'),
	# path('modal/', views.modalpageRender, name='modal'),

	# path('login/', views.loginRender, name='login'),
	path('login/', views.LoginView.as_view(), name='login'),
	# path('register/', views.signupRender, name='register'),
	path('register/', views.RegisterView.as_view(), name='register'),
	path(r'register/facebook-signUp/', include('allauth.urls'), name='facebook-signUp'),

	path('recovery/', views.recoveryRender, name='register'),

	path('logout/', views.LogoutView.as_view(), name='logout'),
]
