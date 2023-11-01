from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import  UserChangePasswordSerializer
from account.renderers import UserRenderer

from account.models import User

class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):

    try:
      user=User.objects.get(email=request.POST['email'])
      if user:
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)
    except:
      return Response({'errors':{'non_field_errors':['User Does not exist']}}, status=status.HTTP_404_NOT_FOUND)
