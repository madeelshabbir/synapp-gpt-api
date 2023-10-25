from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import  UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer, UserUpdateProfileSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
import pdb

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):

    serializer = UserRegistrationSerializer(data=request.data)
    
   
    
    serializer.is_valid(raise_exception=True)
    
    user = serializer.save()
    #token = get_tokens_for_user(user)
    return Response({'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]

  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
 
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      username=user.email
      return Response({'token':token, 'msg':'Login Success', 'username':username}, status=status.HTTP_200_OK)
    else:
     

      return Response({'errors':{'non_field_errors':['Connexion / signing in is not working']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
  def put(self, request, format=None):
      user=User.objects.get(email=request.user)
      
     
      
     
   
     
      password = request.data['password_old']
      email = user.email
      userr = authenticate(email=email, password=password)
      if userr is not None:
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':user})
        serializer.is_valid(raise_exception=True)
        serializer = UserUpdateProfileSerializer(user,data=request.data)
      
        if serializer.is_valid():
           
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      else:
         return Response({'errors':{'non_field_errors':['Your old Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

     
     
     

class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  # permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    
    try:
      user=User.objects.get(email=request.POST['email'])
      if user:  
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)
    except:
      return Response({'errors':{'non_field_errors':['User Does not exist']}}, status=status.HTTP_404_NOT_FOUND)

# class SendPasswordResetEmailView(APIView):
#   renderer_classes = [UserRenderer]
#   def post(self, request, format=None):
#     serializer = SendPasswordResetEmailSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)


