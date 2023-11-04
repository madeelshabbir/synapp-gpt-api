from rest_framework.views import APIView
from rest_framework.response import Response
from  rest_framework import status

from superadmin.serializers import *

class DocumentView(APIView):
  def get(self, request):
    train = PDFFile.objects.filter(status=True).count()
    untrain = PDFFile.objects.filter(status=False).count()
    return Response({"train_docx": train, "untrain_docx": untrain},status=status.HTTP_200_OK)
