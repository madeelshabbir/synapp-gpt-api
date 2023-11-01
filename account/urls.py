from django.contrib import admin
from django.urls import path, include

from account.views.session_view import SessionView
from account.views.user_view import UserView
from account.views.user_login_view import UserLoginView
from account.views.user_registration_view import UserRegistrationView
from account.views.user_change_password_view import UserChangePasswordView
from account.views.user_profile_view import UserProfileView

urlpatterns = [
   path('login/', UserLoginView.as_view(), name='login'),
   path('register/', UserRegistrationView.as_view(), name='register'),
   path('change_password/', UserChangePasswordView.as_view(), name='changepassword'),
   path('profile/', UserProfileView.as_view(), name='get_profile'),
   path('users/session', SessionView.as_view(http_method_names=['post', 'delete'])),
   path('users', UserView.as_view(http_method_names=['post', 'put'])),
]
