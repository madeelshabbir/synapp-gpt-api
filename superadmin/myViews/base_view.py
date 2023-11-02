from rest_framework.views import APIView
from appwrite.client import Client
from appwrite.services.databases import Databases

import environ
import requests

env = environ.Env()
environ.Env.read_env()

class BaseView(APIView):
  def create_client(self):
    client = Client()
    (client
      .set_endpoint(env('APP_WRITE_ENDPOINT'))
      .set_project(env('PROJECT_ID'))
      .set_key(env('PROJECT_SECRET_KEY'))
    )
    return client

  def _authenticate(self, request):
    session_id = request.headers['X-ACCESS-TOKEN']
    session_url = f"{env('APP_WRITE_ENDPOINT')}/account/sessions/{session_id}"

    response = requests.get(session_url, headers={
        "Content-Type": "application/json",
        "X-Appwrite-Project": '64b4cb0d1b60dd5e3a99'
    })

    body = response.json()
    print(body)

  def create_database(self):
    client = self.create_client()
    return Databases(client)

  def create_document(self, collection_id, document_id, body):
    return self.databases.create_document(env('DATABASE_ID'), collection_id, document_id, body)

  def list_documents(self, collection_id, queries):
    return self.databases.get_document(env('DATABASE_ID'), collection_id, queries)
