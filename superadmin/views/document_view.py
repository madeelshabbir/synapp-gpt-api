from rest_framework.response import Response
from  rest_framework import status

from .base_view import BaseView

class DocumentView(BaseView):
  def get(self, request):
    attachments = super().list_files()
    return Response({"train_docx": len(attachments), "untrain_docx": 0},status=status.HTTP_200_OK)
