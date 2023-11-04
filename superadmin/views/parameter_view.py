from rest_framework.response import Response
from rest_framework import status
from appwrite.services.storage import Storage
from appwrite.id import ID
from appwrite.exception import AppwriteException
from appwrite.query import Query

from superadmin.serializers import PdfSerializer
from appwrite.input_file import InputFile
from .base_view import BaseView
from django.conf import settings
import environ
import os

env = environ.Env()
environ.Env.read_env()

class ParameterView(BaseView):
    def get(self, request, format=None):
      databases = super().create_database()
      try:
        parameter = databases.get_document(env('DATABASE_ID'), env('PARAMETER_COLLECTION_ID'), '1')
        return Response({ "parameter": {
            'temperature': parameter['temperature'],
            'topP': parameter['top_p'],
            'modelName': parameter['model_name'],
            'presencePenalty': parameter['presence_penalty'],
            'frequencyPenalty': parameter['frequency_penalty'],
            'maximumLength': parameter['max_length']
          }}, status=status.HTTP_200_OK)
      except AppwriteException as exc:
        return Response({ 'errors': { 'parameter': exc.message } }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def put(self, request, format=None):
      databases = super().create_database()
      request_body = {
        'temperature': request.data.get('temperature'),
        'top_p': request.data.get('topP'),
        'model_name': request.data.get('modelName'),
        'presence_penalty': request.data.get('presencePenalty'),
        'frequency_penalty': request.data.get('frequencyPenalty'),
        'max_length': request.data.get('maximumLength')
      }

      print(request_body)
      request_body = {key: value for key, value in request_body.items() if value is not None}

      try:
        print(request_body)
        result = databases.update_document(env('DATABASE_ID'), env('PARAMETER_COLLECTION_ID'), '1', request_body)
        return Response({'parameter': result}, status=status.HTTP_200_OK)
      except AppwriteException as exc:
        return Response({ 'errors': { 'parameter': exc.message } }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
