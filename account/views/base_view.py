from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status

class BaseView(APIView):
  def _current_user(self, request):
    user = User.objects.get(email=request.user.email)
    user_serializer = UserSerializer(user)
    return Response(user_serializer.data)

  def _authenticate(self, request):
    if not request.user.is_authenticated:
      return unauthenticated_response()

  def _developer(self, request):
    if not request.user.role == 1:
      return unauthorized_response()

  def _recruiter(self, request):
    if not request.user.role == 2:
      return unauthorized_response()

  def _authorize(self, request):
    if not request.user.is_superuser:
      if not request.user.is_staff:
        return unauthorized_response()

  def _self_user_admin(self, request, id):
    return self.check_exists(self._model_name, request.user.id, id)

  def user_authorize(self, model_name):
    return Response({ model_name: 'Success' }, status=status.HTTP_200_OK)

  def _find_resource(self, id):
    try:
      return self._model.objects.get(id=id, is_deleted=False)
    except ObjectDoesNotExist:
      pass

  @property
  def _model(self):
    return eval(self._model_class_name)

  @property
  def _model_name(self):
    return camel_to_snake(self._model_class_name)

  @property
  def _model_class_name(self):
    return type(self).__name__.replace('View', '')
