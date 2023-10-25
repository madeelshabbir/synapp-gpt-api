from django.contrib import admin
from django.urls import path, include
from .views import * 

urlpatterns = [
   path('login/', UserLoginView.as_view(), name='login'),
   path('register/', UserRegistrationView.as_view(), name='register'),
   path('change_password/', UserChangePasswordView.as_view(), name='changepassword'),
   path('profile/', UserProfileView.as_view(), name='get_profile'),
   
]