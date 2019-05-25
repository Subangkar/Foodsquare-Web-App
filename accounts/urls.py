from django.urls import path
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

	path('recovery/', views.recoveryRender, name='register'),

	path('logout/', views.LogoutView.as_view(), name='logout'),
]
