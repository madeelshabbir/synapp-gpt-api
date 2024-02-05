from rest_framework.response import Response
from rest_framework import status
from appwrite.services.users import Users
from django.http import HttpResponse
from appwrite.query import Query
from appwrite.exception import AppwriteException

from .base_view import BaseView
import environ
import csv

env = environ.Env()
environ.Env.read_env()

class UserView(BaseView):
  def _process_csv(self, headers, data, filename):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

    writer = csv.writer(response)
    writer.writerow(headers)
    for i, row in enumerate(data, 1):
        writer.writerow([i] + row)

    return response

  def _process_user_csv(self):
    client = super().create_client()
    users = Users(client)
    result = users.list(queries=[Query.limit(100)])
    user_data = result.get('users', [])
    headers = ['#No', 'Username', 'Email', 'Occupation', 'Specialty']
    data = [
        [
            user['name'],
            user['email'],
            user['prefs'].get('profession', ''),
            user['prefs'].get('speciality', ''),
        ]
        for user in user_data
    ]
    return self._process_csv(headers, data, 'users')

  def _process_question_csv(self):
    databases = super().create_database()
    result = databases.list_documents(
        env('DATABASE_ID'),
        env('USER_CHAT_COLLECTION_ID'),
        queries=[Query.limit(100)]
    )
    question_data = result.get('documents', [])
    headers = ['#id', 'Question', 'Answer', 'Reaction']
    data = [
        [obj['question'], obj['answer'], obj['status']]
        for obj in question_data
    ]
    return self._process_csv(headers, data, 'data')

  def get(self, request):
    if 'csv' in request.path_info:
      return self.generate_csv(request)
    client = super().create_client()
    try:
      users = Users(client)
      result = users.list()
      response_data = []
      for user in result['users']:
        user_info = {
            'name': user.get('name', ''),
            'email': user.get('email', ''),
            'prefs': user.get('prefs', {})
        }
        response_data.append(user_info)
      return Response({'users': response_data}, status=status.HTTP_200_OK)
    except AppwriteException as exc:
      return Response({ 'errors': { 'users': exc.message } }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


  def generate_csv(self, request, format=None):
    model = request.GET.get('model')

    if model == 'user':
        return self._process_user_csv()
    elif model == 'question':
        return self._process_question_csv()
    else:
      return Response({'errors': {'CSV': 'Illegal data request'}}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
