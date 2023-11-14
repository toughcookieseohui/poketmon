from django.db import models
from django.contrib import admin
from django.utils import timezone
# Create your models here.


class monster(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    height = models.FloatField(null=True, default=None)
    classify = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    weight = models.FloatField(null=True, default=None)
    ability = models.CharField(max_length=200, null=True, default=None)
    description = models.CharField(max_length=200)
    evolution = models.CharField(max_length=200)
    img = models.URLField(max_length=200)
