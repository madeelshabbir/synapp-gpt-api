from django.urls import path

from .views.file_view import *
from .views.parameter_view import *
from .views.user_view import *
from .views.question_view import *
from .views.statistical_view import *
from .views.document_view import *
from .views.permission_view import *

urlpatterns = [
    path('question/', QuestionView.as_view(), name='question'),
    path('parameter/', ParameterView.as_view(), name='parameter'),
    path('statistics/', StatisticalView.as_view()),
    path('document/', DocumentView.as_view()),
    path('files/', FileView.as_view()),
    path('users/', UserView.as_view(), name='user-list'),
    path('users/csv/', UserView.as_view(), name='generate-csv'),
    path('questions/', QuestionView.as_view()),
    path('permissions/', PermissionView.as_view())
]
