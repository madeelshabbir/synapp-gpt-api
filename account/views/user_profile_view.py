from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import  UserChangePasswordSerializer,UserProfileSerializer, UserUpdateProfileSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from account.models import User

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
