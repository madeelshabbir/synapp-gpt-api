from rest_framework.views import APIView
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
import environ

class BaseView(APIView):
  def __init__(self):
    super().__init__()
    self.env = environ.Env()
    self.env.read_env()
    self.client = self.create_client()
    self.database = self.create_database()
    self.storage = Storage(self.client)

  def create_client(self):
    client = Client()
    (client
      .set_endpoint(self.env('APP_WRITE_ENDPOINT'))
      .set_project(self.env('PROJECT_ID'))
      .set_key(self.env('PROJECT_SECRET_KEY'))
    )
    return client

  def create_database(self):
    return Databases(self.client)

  def create_document(self, collection, document, body = {}):
    return self.database.create_document(self.env('DATABASE_ID'), self.env(collection), document, body)

  def list_documents(self, collection, queries = []):
    return self.database.list_documents(self.env('DATABASE_ID'), self.env(collection), queries)

  def get_document(self, collection, document_id, queries = []):
    return self.database.get_document(self.env('DATABASE_ID'), self.env(collection), document_id, queries)

  def update_document(self, collection, document_id, body = {}):
    return self.database.update_document(self.env('DATABASE_ID'), self.env(collection), document_id, body)

  def list_files(self, pdf_filename = '', queries = []):
    attachments = []
    if pdf_filename is not '':
      result = self.storage.list_files(bucket_id=self.env('TRAINING_BUCKET_ID'), queries=queries, search=pdf_filename)
    else:
      result = self.storage.list_files(bucket_id=self.env('TRAINING_BUCKET_ID'))
    for file in result['files']:
      attachments.append(self.env('ATTACHMENT_PATH')+file['$id']+"/view?project="+ self.env('PROJECT_ID'))
    return attachments
