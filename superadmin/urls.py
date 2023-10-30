from django.urls import path
from .views import *
#import AllUserProfileView, UploadFileView, QuestionView, ParameterView, SubcriberView, SubcriberViewForUnSub
urlpatterns = [
    path('get-all-user/', AllUserProfileView.as_view(), name='all_user'),
    path('upload-file/', UploadFileView.as_view(), name='upload-file'),
    path('question/', QuestionView.as_view(), name='question'),
    path('parameter/', ParameterView.as_view(), name='parameter'),
    path('subcriber/', SubcriberView.as_view(), name='subcriber'),
    path('anonymous-user/', AnnonymusUserCount.as_view(), name='anonymous-user'),
    path('chart-data/', ChartDataView.as_view(), name='chart-data'),
    path('user-export-csv/', UserCSVFile.as_view(), name='user-csv'),
    path('alldata-export-csv/', DataCSVFile.as_view(), name='data-csv'),
    path('chat-history/', ChatHistory.as_view(), name='chat-history'),
    path('get-file/', GetFileView.as_view(), name='get-file'),
    path('view-file/<int:file_id>/', GetPDFFileView.as_view(), name='view-file'),
    path('document-view/', GetDocumentView.as_view(), name='docuemnt-view'),
    path('update-profile/', UserProfileView.as_view(), name='update-profile'),
]
