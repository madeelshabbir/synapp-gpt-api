from django.db import models

# Create your models here.
from django.db import models
from account.models import User
from django.db.models import Sum

def upload_to(instance, filename):
    # Define the destination directory for the uploaded files
    return f'files_data/{filename}'

class PDFFile(models.Model):
    file = models.FileField(upload_to=upload_to)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.file.name
class Parameter(models.Model):
    temperture = models.FloatField()
    max_length = models.IntegerField()
    frequency_penalty = models.FloatField()
    presence_penalty = models.FloatField()
    top_p = models.FloatField() 
    model_name = models.CharField(max_length=200)
    def __str__(self):
        return self.model_name
class Subcriber(models.Model):
    subcriber = models.IntegerField()
    unsubcriber = models.IntegerField()
class Countsubcriber(models.Model):
    ip_address = models.CharField(max_length=100)
    count = models.IntegerField()
    created_at = models.DateField()
    def __str__(self):
        return self.ip_address
    def get_total_count_for_date(ip_address):
        total_count = Countunsubcriber.objects.filter(ip_address=ip_address).aggregate(Sum('count'))
        return total_count['count__sum'] or 0

class Countunsubcriber(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    count = models.IntegerField()
    created_at = models.DateField()
    def __int__(self):
        return self.user
    def get_total_count_for_date(date):
        total_count = Countunsubcriber.objects.filter(created_at=date).aggregate(Sum('count'))
        return total_count['count__sum'] or 0
class Statistic(models.Model):
    count = models.IntegerField()
    created_at = models.DateField()
    day = models.CharField(max_length=100)
    def __int__(self):
        return self.count
class Userchat(models.Model):
    user_info = models.CharField(max_length=100)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateField()
    status = models.IntegerField(null=True, default=-1)
    def __str__(self):
        return self.user_info
    

  
 

     

