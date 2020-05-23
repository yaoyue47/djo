from django.db import models

# Create your models here.
from django.db.models import CASCADE


class User(models.Model):
    user_name = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)


class Shumeipai(models.Model):
    name = models.CharField(unique=True, max_length=200)
    status = models.BooleanField(default=True)
    remarks = models.CharField(max_length=200, default="暂无备注")
    user_shumeipai = models.ForeignKey(User, on_delete=CASCADE)


class Main_data(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    humidity = models.FloatField()
    name = models.ForeignKey(Shumeipai, on_delete=CASCADE, db_index=True)


class System_inf(models.Model):
    click_time = models.IntegerField()
