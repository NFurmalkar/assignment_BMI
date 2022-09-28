from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Details(models.Model):
    id = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    height = models.CharField(max_length=50)
    weight = models.CharField(max_length=50)
    bmi = models.CharField(max_length=50,default="")
