from http.client import NOT_FOUND
from django.shortcuts import render
from rest_framework.views import APIView
from account.models import User
#from .serializers import UserAllProfileSerializer, PdfSerializer, ParameterSerializer, SubcriberSerializer
from  rest_framework import status
from rest_framework.response import Response
from .models import Parameter, Subcriber, Countsubcriber, Countunsubcriber, Statistic, Userchat
from .serializers import*
from synappgpt.module import load_data, answer

from django.conf import settings
from account.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated ,AllowAny
from datetime import date, timedelta
from django.db.models import Sum
from datetime import datetime, timedelta
from django.http import FileResponse
import calendar
import re
from appwrite.id import ID
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.users import Users
import time

import socket
import csv
from django.http import HttpResponse



import pdb
import os
import requests


client = Client()
(client
  .set_endpoint('https://cloud.appwrite.io/v1') # Your API Endpoint
  .set_project('64b4cb0d1b60dd5e3a99') # Your project ID
  .set_key('6215fadd1276e8de8f57b445b583450fb76283d4984dfff4c47e0cf188cd890d0efb4feb420403e5a83f6e73f45f47724af028472a2c6c27453a2e42e1109ee7f80937d2e087460cc4617ff53a20cbf356e731fe615bcb089dcadb7dd5207691e528347b215d5e9c8d94e8fd287b0718a9bb513161510b020e35fa01ed873dbf') # Your secret API key
)
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        data = response.json()
        public_ip = data['ip']
        print("MY PUBLIC IP: "+public_ip)
        return public_ip
    except requests.RequestException:
        return None
def calculate_days_statistic(data):
    today = datetime.now().date()

# Create a list to store the count values for the last 7 days


# Iterate over the last 7 days
    count_sum_by_interval = {}
    for i in range(7):
      # Calculate the date for each day
        date = today - timedelta(days=i)



      # Find the data for the current date, if it exists
        day_data = next((d for d in data if d['created_at'].split('T')[0] == str(date)), None)

      # If data exists for the current date, add its count value to the result list
        day_of_week = date.strftime("%A")
        if day_data:

            count_sum_by_interval[day_of_week]=day_data['count']
        # If data does not exist for the current date, add 0 to the result list
        else:
            count_sum_by_interval[day_of_week]=0



    current_day = datetime.now().strftime('%A')
    days_of_week = list(calendar.day_name)
    days_of_week = days_of_week[days_of_week.index('Monday'):] + days_of_week[:days_of_week.index('Monday')]
    # Create a new list to store the ordered values
    ordered_values = []
    for day in days_of_week:
        ordered_values.append(count_sum_by_interval.get(day, 0))

    return ordered_values
def calculate_month_statistic(data):
    latest_month = data[-1]['created_at'].split('-')[1]

    # Create a dictionary to store the sum of 'count' values for each four-week interval
    count_sum_by_interval = {}

    # Initialize count values for all four intervals of the month to 0
    for interval in range(1, 5):
        interval_key = f"{latest_month}-{interval}"
        count_sum_by_interval[interval_key] = 0

    # Iterate over each item in the data
    for item in data:
        date_str = item['created_at'].split('T')[0]  # Extract date part 'YYYY-MM-DD'
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        month = date_obj.strftime('%m')
        day = date_obj.day
        count = item['count']

        # Check if the month matches the latest month
        if month == latest_month:
            print("ok")
            # Calculate the four-week interval number for the date
            interval = (day - 1) // 7 + 1
            #interval = 1

            # Create a key for the interval combining the month and interval number
            interval_key = f"{month}-{interval}"

            # Update the count value for the interval
            count_sum_by_interval[interval_key] += count

    # Print the sum of 'count' values for each four-week interval
    list_for_month = []
    for interval, count_sum in count_sum_by_interval.items():
        list_for_month.append(count_sum)

    return list_for_month

def calculate_year_statistic(data):

    count_sum_by_month = {}

      # Iterate over each item in the data

    for item in data:
        date_partss = item['created_at'].split('T')[0]
        date_parts = date_partss.split('-')

        month = date_parts[1]
        count = item['count']

      # Check if the month already exists in the dictionary
        if month in count_sum_by_month:
            count_sum_by_month[month] += count
        else:
            count_sum_by_month[month] = count

    # Create a list for each month of the year
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    count_by_month_list = [count_sum_by_month.get(month, 0) for month in months]

    # Print the list of 'count' values for each month
    list_for_year=[]
    for month, count in zip(months, count_by_month_list):
      #print(f"Month {month}: {count}")
      list_for_year.append(count)



    return list_for_year
class AllUserProfileView(APIView):

  # renderer_classes = [UserRenderer]
  # permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    # all_users = User.objects.filter(is_admin=False)  # Use filter instead of exclude
    # serializer = UserAllProfileSerializer(all_users, many=True)
    client = Client()
    (client
      .set_endpoint('https://cloud.appwrite.io/v1') # Your API Endpoint
      .set_project('64b4cb0d1b60dd5e3a99') # Your project ID
      .set_key('6215fadd1276e8de8f57b445b583450fb76283d4984dfff4c47e0cf188cd890d0efb4feb420403e5a83f6e73f45f47724af028472a2c6c27453a2e42e1109ee7f80937d2e087460cc4617ff53a20cbf356e731fe615bcb089dcadb7dd5207691e528347b215d5e9c8d94e8fd287b0718a9bb513161510b020e35fa01ed873dbf') # Your secret API key
    )

    users = Users(client)

    result = users.list()
    data =result['users']
    return Response(data, status=status.HTTP_200_OK)
class GetFileView(APIView):
  def get(self, request, format=None):
    pdf_path =  os.path.join(settings.MEDIA_ROOT, 'files_data/*.pdf')
    pdf = PDFFile.objects.all();
    serializer = NewPdfSerializer(pdf,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
class GetPDFFileView(APIView):
    def get(self, request, file_id, *args, **kwargs):
        try:
            pdf_file = PDFFile.objects.get(id=file_id)
            response = FileResponse(pdf_file.file, content_type='application/pdf')
            return response
        except PDFFile.DoesNotExist:
            return HttpResponse(status=404)
class GetDocumentView(APIView):
  # renderer_classes = [UserRenderer]
  # permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    train_ = PDFFile.objects.filter(status=True).count()
    untrain_ = PDFFile.objects.filter(status=False).count()
    return Response({"train_docx":train_,"untrain_docx":untrain_},status=status.HTTP_200_OK)


class UploadFileView(APIView):
  # renderer_classes = [UserRenderer]
  # permission_classes = [IsAuthenticated]

  # def get(self, request, format=None):
  #   pdf_path =  os.path.join(settings.MEDIA_ROOT, 'data/*.pdf')
  #   pdf = PDFFile.objects.all();
  #   serializer = PdfSerializer(pdf,many=True)
  #   return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):


      #file = request.FILES.getlist('file')
      pdf_path =  os.path.join(settings.MEDIA_ROOT, 'data')



      # folder_path = '/path/to/folder'  # Specify the path to your folder containing the PDF files

      # for filename in os.listdir(pdf_path):
      #     if filename.endswith('.pdf'):
      #         file_path = os.path.join(pdf_path, filename)
      #         os.remove(file_path)
      #         print(f"Deleted file: {file_path}")




      file = request.FILES.getlist('files[]')


      serializer = PdfSerializer(data={'file': file})

      if serializer.is_valid():
          serializer.save()
          return Response({'message': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)

      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionView(APIView):
    # renderer_classes = [UserRenderer]
    # permission_classes = [AllowAny]

    def post(self, request, format=None):
      try:
        objects_to_delete = PDFFile.objects.filter(id__in=[68,69])
        objects_to_delete.delete()
      except:
        pass
      # pdb.set_trace()
     # pdf_path =  os.path.join(settings.MEDIA_ROOT, 'files_data/*.pdf')

      start_time_function = time.time()
      print("start_time",start_time_function)
      parameter = Parameter.objects.filter(id=1).last()

      today = date.today()
      public_ip = ''

      if 'ip_address' in request.data:
         public_ip = request.POST.get('ip_address')
         if not public_ip:
            public_ip = get_public_ip()



      current_day_name = today.strftime("%A")
      day = current_day_name.upper()


      collection_id ='64b543388c228bcdb92f'
      collection_name = 'statistical'


      client = Client()

      (client
        .set_endpoint('https://cloud.appwrite.io/v1') # Your API Endpoint
        .set_project('64b4cb0d1b60dd5e3a99') # Your project ID
        .set_key('6215fadd1276e8de8f57b445b583450fb76283d4984dfff4c47e0cf188cd890d0efb4feb420403e5a83f6e73f45f47724af028472a2c6c27453a2e42e1109ee7f80937d2e087460cc4617ff53a20cbf356e731fe615bcb089dcadb7dd5207691e528347b215d5e9c8d94e8fd287b0718a9bb513161510b020e35fa01ed873dbf') # Your secret API key
      )
      databases = Databases(client)
      try:
        result = databases.get_document('64b5432b9e32fda9235a', '64b543388c228bcdb92f',str(today))
        count =result['count']
        count =count+1
        result = databases.update_document('64b5432b9e32fda9235a', '64b543388c228bcdb92f',str(today) ,{"count":count})
        result = databases.get_document('64b5432b9e32fda9235a', '64b543388c228bcdb92f',str(today))
      except:
          current_day_name = today.strftime("%A")
          day = current_day_name.upper()
          databases.create_document('64b5432b9e32fda9235a', '64b543388c228bcdb92f',str(today), {"count":1,"day":day,"created_at":str(today)})

      question = request.POST.get('question')
      print("Question",question)
      path=settings.MEDIA_ROOT
      complete_path=path.split("/media")[0]
      save_path =  os.path.join(complete_path, 'synappgpt/model_directory')
      message_id =''

      try:
        start_time = time.time()
        print("first difference", start_time - start_time_function)
        print("start_time", start_time)

        response_answer = answer(question, save_path, parameter)

        end_time = time.time()  # Define end_time here

        time_difference = end_time - start_time
        print("difference", time_difference)


        if response_answer:
          if 'ip_address' in request.data:
            #  Userchat.objects.create(user_info=public_ip,question=question,answer=response_answer['result'],created_at=today)
            #  obj=Userchat.objects.filter(user_info=public_ip).last()
            resultt=databases.create_document('64b5432b9e32fda9235a', '64b641e090dc4b18246a',ID.unique(), {"user_info":public_ip,"question":question,"answer":response_answer['result'],"status":-1,"created_at":str(today)})
            message_id=resultt['$id']

          elif 'username' in request.data:
            username = request.POST.get('username')
            #  Userchat.objects.create(user_info=username,question=question,answer=response_answer['result'],created_at=today)
            #  obj=Userchat.objects.filter(user_info=username).last()
            resultt=databases.create_document('64b5432b9e32fda9235a', '64b641e090dc4b18246a',ID.unique(), {"user_info":username,"question":question,"answer":response_answer['result'],"status":-1,"created_at":str(today)})
            message_id=resultt['$id']

            #message_id=obj.id

      except:
         response_answer['result']="Some Error Occure from API"
         pass
      end_time = time.time()

      if response_answer['sources']:
        return Response({'data':response_answer['result'],'sources': response_answer['sources'], 'id':message_id,'msg':'Your Answer', 'question':question}, status=status.HTTP_200_OK)
      else:
        return Response({'data':response_answer['result'], 'id':message_id,'msg':'Your Answer',"question":question}, status=status.HTTP_200_OK)

class ParameterView(APIView):
    # renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
      parameter = Parameter.objects.filter(id=1)

      serializer = ParameterSerializer(parameter, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, format=None):
        parameter = Parameter.objects.get(id=1)
        serializer = ParameterSerializer(parameter, data=request.data)
        pdf_path =  os.path.join(settings.MEDIA_ROOT, 'files_data/*.pdf')

        path=settings.MEDIA_ROOT
        complete_path=path.split("/media")[0]
        save_path =  os.path.join(complete_path, 'synappgpt/model_directory')
        if serializer.is_valid():
            serializer.save()
            try:
              load_data(pdf_path,save_path)
              pdf_file =PDFFile.objects.filter(status=False)
              pdf_file.update(status=True)

            except:
               return Response({"error","Error in training Model"}, status=status.HTTP_400_BAD_REQUEST)
               pass


            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class SubcriberView(APIView):
    # renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
      subcriber = Subcriber.objects.filter(id=1)

      serializer = SubcriberSerializer(subcriber, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, format=None):
        subcriber = Subcriber.objects.get(id=1)
        serializer = SubcriberSerializer(subcriber, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class SubcriberViewForUnSub(APIView):
    def get(self, request, format=None):
      subcriber = Subcriber.objects.filter(id=1)

      serializer = SubcriberSerializer(subcriber, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
class AnnonymusUserCount(APIView):
    # renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
      total_unique_unsubscribers = Userchat.objects.filter(user_info__regex=r'^[\d.]+$').values("user_info").distinct()
      total_unique_unsubscribers = total_unique_unsubscribers.count()
      #unique_subscribers = Countsubcriber.objects.values('ip_address').distinct()
      return Response({'data':total_unique_unsubscribers}, status=status.HTTP_200_OK)
class ChartDataView(APIView):
    # renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
      # statistic_data = Statistic.objects.all()
      # serializer = StaticSerializer(statistic_data, many=True)
      # data=serializer.data
      client = Client()
      (client
        .set_endpoint('https://cloud.appwrite.io/v1') # Your API Endpoint
        .set_project('64b4cb0d1b60dd5e3a99') # Your project ID
        .set_key('6215fadd1276e8de8f57b445b583450fb76283d4984dfff4c47e0cf188cd890d0efb4feb420403e5a83f6e73f45f47724af028472a2c6c27453a2e42e1109ee7f80937d2e087460cc4617ff53a20cbf356e731fe615bcb089dcadb7dd5207691e528347b215d5e9c8d94e8fd287b0718a9bb513161510b020e35fa01ed873dbf') # Your secret API key
      )
      databases = Databases(client)
      result = databases.list_documents('64b5432b9e32fda9235a', '64b543388c228bcdb92f')

      data=result['documents']

      year_data = calculate_year_statistic(data)
      month_data = calculate_month_statistic(data)
      days_data = calculate_days_statistic(data)
      users = Users(client)

      result = users.list()
      #print("results",result['total'])

      return Response({'days':days_data,'year':year_data,'month':month_data,'total_user':result['total']} ,status=status.HTTP_200_OK)

class UserCSVFile(APIView):
 def get(self, request, format=None):
    # renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]


    client = Client()
    (client
      .set_endpoint('https://cloud.appwrite.io/v1') # Your API Endpoint
      .set_project('64b4cb0d1b60dd5e3a99') # Your project ID
      .set_key('6215fadd1276e8de8f57b445b583450fb76283d4984dfff4c47e0cf188cd890d0efb4feb420403e5a83f6e73f45f47724af028472a2c6c27453a2e42e1109ee7f80937d2e087460cc4617ff53a20cbf356e731fe615bcb089dcadb7dd5207691e528347b215d5e9c8d94e8fd287b0718a9bb513161510b020e35fa01ed873dbf') # Your secret API key
    )

    users = Users(client)

    result = users.list()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['Username', 'Email', 'Occupation', 'Specialty'])

    #users = User.objects.all().exclude(is_admin=True)

    users =result['users']
    for user in users:
      profession=''
      specity = ' '
      if user['prefs']:
        try:
          profession=user['prefs']['profession']
          specity=user['prefs']['speciality']
        except:
            pass

      writer.writerow([user['name'], user['email'], profession, specity])

    return response
class DataCSVFile(APIView):
 def get(self, request, format=None):
    # renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]
    client = Client()
    (client
      .set_endpoint('https://cloud.appwrite.io/v1') # Your API Endpoint
      .set_project('64b4cb0d1b60dd5e3a99') # Your project ID
      .set_key('6215fadd1276e8de8f57b445b583450fb76283d4984dfff4c47e0cf188cd890d0efb4feb420403e5a83f6e73f45f47724af028472a2c6c27453a2e42e1109ee7f80937d2e087460cc4617ff53a20cbf356e731fe615bcb089dcadb7dd5207691e528347b215d5e9c8d94e8fd287b0718a9bb513161510b020e35fa01ed873dbf') # Your secret API key
    )
    databases = Databases(client)
    result = databases.list_documents('64b5432b9e32fda9235a', '64b641e090dc4b18246a')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    writer = csv.writer(response)
    writer.writerow(['#id', 'Question', 'Answer', 'Reaction'])

    #question_data = Userchat.objects.all()
    question_data =result['documents']
    for i, obj in enumerate(question_data, 1):
        writer.writerow([i, obj['question'], obj['answer'], obj['status']])

    return response
class GetChatHistory(APIView):

    def get(self, request, format=None):
      chat_data = Userchat.objects.all()
      serializer = UserChatSerializer(chat_data, many=True)
      data=serializer.data
      return Response({'data':data} ,status=status.HTTP_200_OK)

    def post(self, request, format=None):


      if 'username' in request.data:
          username = request.data['username']
          today = date.today()

         # result=databases.list_documents('64b5432b9e32fda9235a', '64b641e090dc4b18246a', {"user_info":public_ip,"question":question,"answer":response_answer['result'],"status":-1,"created_at":str(today)})
          data = Userchat.objects.filter(user_info=username,created_at=today)
          serializer = UserChatSerializer(data, many=True)
          return Response({'data': serializer.data}, status=status.HTTP_200_OK)
      elif 'ip_address' in request.data:
          public_ip = request.data['ip_address']
          if not public_ip:
              public_ip = get_public_ip()
          data = Userchat.objects.filter(user_info=public_ip)
          serializer = UserChatSerializer(data, many=True)
          return Response({'data': serializer.data}, status=status.HTTP_200_OK)
      return Response({'data': "Not found"}, status=status.HTTP_204_NO_CONTENT)
    def put(self, request, format=None):
        messageid=request.data['messageid']

        chat = Userchat.objects.get(id=messageid)
        serializer = UserChatSerializer(chat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):


  def put(self, request, format=None):
    users = Users(client)
    password = request.data['password']
    userid = request.data['userid']
    profession = request.data['occupation']
    password_old = request.data['password_old']
    specialty = request.data['specialty']
    result = users.update_prefs(userid, {"profession":profession,"specialty":specialty})
    print("result",result)
    if result:
      result1 = users.update_password(userid,password)
      if result1:
        return Response(result, status=status.HTTP_200_OK)
      else:
         return Response(result, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)









