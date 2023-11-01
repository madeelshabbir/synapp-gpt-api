import environ
env = environ.Env()
environ.Env.read_env()

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework import status

import requests
import json
from .base_view import BaseView

class SessionView(BaseView):
  def post(self, request):
    email = request.data.get('email')
    password = request.data.get('password')
    jwt = request.headers('X-JWT-TOKEN')
    if 'email' not in request.data or 'password' not in request.data:
      return Response({ 'errors': { 'user': ['Missing parameters.'] } }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    print(jwt)
    session_url = f"{env('APP_WRITE_ENDPOINT')}/account/sessions"

    payload = {
      "email": email,
      "password": password
    }

    response = requests.post(session_url, data=json.dumps(payload), headers={
        "Content-Type": "application/json",
        "X-Appwrite-Project": '64b4cb0d1b60dd5e3a99',
        "X-Appwrite-JWT": jwt
    })

    body = response.json()
    if response.status_code == status.HTTP_201_CREATED:
        return Response({'session': {'session_id': body['$id']}}, status=status.HTTP_200_OK)
    else:
      return Response({ 'errors': { 'session': [body['message']] } }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

  def delete(self, request):
    authorize = self._authenticate(request)
    # if authorize is not True:
    #   return authorize

    # try:
    #   token = RefreshToken.for_user(request.user)
    #   token.blacklist()
    #   logout(request)
    #   return Response({'user': 'User logged out successfully'}, status=status.HTTP_200_OK)
    # except:
    return Response({ 'errors': { 'user': ['Something went wrong!'] } }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


  def __get_tokens_for_user(self, user):
    refresh = RefreshToken.for_user(user)
    return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
    }
