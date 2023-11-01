from rest_framework.response import Response
from rest_framework import status
from appwrite.services.users import Users
from appwrite.id import ID
from appwrite.exception import AppwriteException

from .base_view import BaseView
import environ
import requests
import json
env = environ.Env()
environ.Env.read_env()

class UserView(BaseView):
  def post(self, request):
    email = request.data.get('email')
    password = request.data.get('password')
    is_cgu = request.data.get('is_cgu')
    is_pdp = request.data.get('is_pdp')
    name = request.data.get('name', email.split('@')[0])
    speciality = request.data.get('speciality')
    profession = request.data.get('profession')
    is_admin = request.data.get('is_admin', False)

    if not (email and password and is_cgu and is_pdp):
      return Response({'errors': {'user': ['Missing parameters.']}}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    if is_cgu is 'False' or is_pdp is 'False':
      return Response({ 'errors': { 'user': {
        'is_pdp': 'Must be true for registration',
        'is_cgu': 'Must be true for registration'
      }} }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    is_cgu = is_cgu.lower() == 'true'
    is_pdp = is_pdp.lower() == 'true'

    try:
      client = super().create_client()
      users = Users(client)
      result = users.create(ID.unique(), email, None, password, name)

      print(result)
      user_prefs = {
          'speciality': speciality,
          'profession': profession,
          'is_cgu': is_cgu,
          'is_pdp': is_pdp,
          'is_admin': is_admin,
      }
      users.update_prefs(result['$id'], user_prefs)

      return Response({'user': {'email': email, 'message': 'User created successfully'}}, status=status.HTTP_201_CREATED)
    except AppwriteException as exc:
      return Response({ 'errors': { 'user': exc.message } }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


# Define the API endpoint, hostname, and project ID
    # api_endpoint =f"{env('APP_WRITE_ENDPOINT')}/account"
    # project_id = env('PROJECT_ID')

    # # Define the payload
    # payload = {
    #     "userId": ID.unique(),
    #     "email": email,
    #     "password": password,
    #     "name": name
    # }

    # # Define the headers
    # headers = {
    #     "Content-Type": "application/json",
    #     "X-Appwrite-Project": project_id
    # }

    # # Make the POST request
    # response = requests.post(api_endpoint, json=payload, headers=headers)

    # # Check the response
    # if response.status_code == 200:
    #     print("User account created successfully")
    # else:
    #     print(f"Failed to create user account. Status code: {response.status_code}")
    #     print(response.text)
    # return Response({'user': {'email': email, 'message': 'User updated successfully'}}, status=status.HTTP_200_OK)

  def put(self, request):
    authorize = super()._authenticate(request)
    if authorize is not True:
      return authorize

    client = super().create_client()
    users = Users(client)
    password = request.data.get('password')
    user_id = request.data.get('user_id')
    email = request.data.get('email')
    speciality = request.data.get('speciality')
    profession = request.data.get('profession')

    user_prefs = {
      'speciality': speciality,
      'profession': profession
    }

    try:
      users.update_prefs(user_id, user_prefs)
      if password:
        users.update_password(user_id, password)
      return Response({'user': {'email': email, 'message': 'User updated successfully'}}, status=status.HTTP_200_OK)
    except AppwriteException as exc:
      return Response({ 'errors': { 'user': exc.message } }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
