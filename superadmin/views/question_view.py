from rest_framework.response import Response
from rest_framework import status
from appwrite.query import Query
from appwrite.exception import AppwriteException
from appwrite.id import ID
from datetime import date
from django.conf import settings
import time
import requests
import re
import os

from .base_view import BaseView
from synappgpt.module import *
from superadmin.constants.endpoints import *
from superadmin.constants.regex import *
from superadmin.wrappers.dot_notation_object import *

class QuestionView(BaseView):
  def _get_public_ip(self):
    try:
      response = requests.get(IPIFY_API_ENDPOINT)
      data = response.json()
      public_ip = data['ip']
      print("MY PUBLIC IP: " + public_ip)
      return public_ip
    except requests.RequestException:
      return None

  def get(self, request):
    query = request.query_params.get('query', None)
    queries = [Query.limit(100)]
    try:
      if query:
        today = date.today().strftime('%Y-%m-%d')
        queries = [Query.equal('user_info', query), Query.order_desc('prompt_id')]
        if re.match(IP, query):
          queries.append(Query.equal('created_at', today))
        print(queries)
      res = super().list_documents('USER_CHAT_COLLECTION_ID', queries)

      ip_count = 0
      email_count = 0
      for document in res["documents"]:
        user_info = document["user_info"]
        if re.match(IP, user_info):
          ip_count += 1
        else:
          email_count += 1

      res['anonymous'] = ip_count
      res['subscribed'] = email_count

      return Response({"questions": res}, status=status.HTTP_200_OK)
    except AppwriteException as exc:
      return Response({ 'errors': { 'questions': exc.message } }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

  def post(self, request):
    start_time_function = time.time()
    print("start_time", start_time_function)
    today = date.today()
    public_ip = ''
    prompt_id = request.POST.get('prompt_id')
    if 'ip_address' in request.data:
      public_ip = request.POST.get('ip_address')
      if not public_ip:
        public_ip = self._get_public_ip()

    current_day_name = today.strftime("%A")
    day = current_day_name.upper()

    try:
      result = super().get_document('STATISTICAL_COLLECTION_ID', str(today))
      count = result['count']
      count = count + 1
      result = super().update_document('STATISTICAL_COLLECTION_ID', str(today), { "count": count })
      result = super().get_document('STATISTICAL_COLLECTION_ID', str(today))
    except:
      current_day_name = today.strftime("%A")
      day = current_day_name.upper()
      super().create_document('STATISTICAL_COLLECTION_ID', str(today), { "count": 1, "day": day, "created_at": str(today) })

    question = request.POST.get('question')
    print("Question", question)
    path = settings.MEDIA_ROOT
    complete_path = path.split("/media")[0]
    save_path = os.path.join(complete_path, 'synappgpt/model_directory')
    message_id = ''

    parameter = super().get_document('PARAMETER_COLLECTION_ID', '1')
    parameter = DotNotationObject(parameter)
    try:
      start_time = time.time()
      print("first difference", start_time - start_time_function)
      print("start_time", start_time)
      response_answer = answer(question, save_path, parameter)
      print(response_answer)
      end_time = time.time()

      time_difference = end_time - start_time
      print("difference", time_difference)

      request_obj = {
        "question": question,
        "answer": response_answer['result'],
        "status": -1,
        "created_at": str(today)
      }
      if response_answer:
        if 'ip_address' in request.data:
          user_info = public_ip
        elif 'username' in request.data:
          user_info = request.POST.get('username')

        if prompt_id == '':
          prompt = super().create_document('PROMPT_COLLECTION_ID', ID.unique(),
                                                {"user_info": user_info, "created_at": str(today)})
          prompt_id = prompt['$id']
          request_obj['prompt_id'] = prompt_id
        else:
          request_obj['prompt_id'] = prompt_id
        if response_answer['sources']:
          pdf_filenames = response_answer.get('sources', set())

          for pdf_filename in pdf_filenames:
            queries = [Query.equal('name', pdf_filename)]
            attachments = super().list_files(pdf_filename, queries)
          request_obj["attachments"] = ', '.join(attachments)
          request_obj["sources"] = ', '.join(pdf_filenames)

        request_obj['user_info'] = user_info
        print(request_obj)
        resultt = super().create_document('USER_CHAT_COLLECTION_ID', ID.unique(), request_obj)
        message_id = resultt['$id']
        print(request_obj)
    except Exception as exc:
      print(exc)
      response_answer['result'] = "Some Error Occurred from API"
      pass
    end_time = time.time()

    if response_answer['sources']:
      return Response({'data': response_answer['result'],
                        'sources': response_answer['sources'],
                        'id': message_id,
                        'msg': 'Your Answer',
                        'attachments': attachments,
                        'question': question,
                        'prompt_id': prompt_id},
                      status=status.HTTP_200_OK)
    else:
      return Response({'data': response_answer['result'], 'id': message_id, 'msg': 'Your Answer', "question": question, 'prompt_id': prompt_id},
                        status=status.HTTP_200_OK)

  def put(self, request):
    id, like = request.data.get('id'), request.data.get('status')
    if id:
      result = super().update_document('USER_CHAT_COLLECTION_ID', id, {'status': like})
      return Response(result, status=status.HTTP_200_OK)
    else:
      return Response({"error","Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

