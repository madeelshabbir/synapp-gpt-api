from django.contrib import admin
from .models import Parameter, Subcriber, Countsubcriber, Countunsubcriber, Statistic, Userchat

admin.site.register(Parameter)
admin.site.register(Subcriber)
admin.site.register(Countsubcriber)
admin.site.register(Countunsubcriber)
admin.site.register(Statistic)
admin.site.register(Userchat)
# Register your models here.
