from rest_framework.response import Response
from rest_framework import status
from appwrite.exception import AppwriteException

from .base_view import BaseView

class PermissionView(BaseView):
  def get(self, request, format=None):
    try:
      result = super().get_document('PERMISSION_COLLECTION_ID', '1')
      return Response({ "permissions": {
            'subscriber': result['subcriber'],
            'unsubscriber': result['unsubcriber']
          }}, status=status.HTTP_200_OK)
    except AppwriteException as exc:
      return Response({ 'errors': { 'permissions': exc.message } }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

  def put(self, request, format=None):
    request_body = {
      'subcriber': request.data.get('subscriber'),
      'unsubcriber': request.data.get('unsubscriber')
    }

    request_body = {key: value for key, value in request_body.items() if value is not None}

    try:
      result = super().update_document('PERMISSION_COLLECTION_ID', '1', request_body)
      return Response({ "permissions": {
            'subscriber': result['subcriber'],
            'unsubscriber': result['unsubcriber']
          }}, status=status.HTTP_200_OK)
    except AppwriteException as exc:
      return Response({ 'errors': { 'permissions': exc.message } }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
