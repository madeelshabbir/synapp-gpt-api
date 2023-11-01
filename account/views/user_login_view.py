from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import  UserLoginSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]

  def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

  def post(self, request, format=None):
    print('Hi, in post')
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
