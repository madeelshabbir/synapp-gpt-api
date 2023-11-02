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

class FileView(BaseView):
  def get(self, request):
    try:
      client = super().create_client()
      storage = Storage(client)
      attachments = []
      result = storage.list_files(bucket_id=env('TRAINING_BUCKET_ID'), queries=[Query.limit(100)])
      for file in result['files']:
        attachments.append({'name': file['name'], 'path': env('ATTACHMENT_PATH')+file['$id']+"/view?project="+env('PROJECT_ID')})
      return Response({'files': attachments}, status=status.HTTP_200_OK)
    except AppwriteException as exc:
      return Response({ 'errors': { 'files': exc.message } }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

  def post(self, request, format=None):
    files = request.FILES.getlist('files[]')
    serializer = PdfSerializer(data={'file': files})
    client = super().create_client()

    if serializer.is_valid():
      resp = serializer.save()
      file_paths = [pdf_file.file.name for pdf_file in resp]
      for f in files:
        storage = Storage(client)
        file_info = storage.create_file(
            env('TRAINING_BUCKET_ID'),
            file_id='unique()',
            file=InputFile.from_path(os.path.join(settings.MEDIA_ROOT, file_paths[0]))
        )
        print(f'File uploaded to Appwrite with ID: {file_info["$id"]}')
      return Response({'files': { 'name': file_paths[0].split('files_data/')[1], 'path': env('ATTACHMENT_PATH')+file_info['$id']+"/view?project="+env('PROJECT_ID')}}, status=status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
