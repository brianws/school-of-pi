from django.conf import settings
from django.db import models
from django.utils import timezone

class School(models.Model):
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    code = models.CharField(max_length=15, default='Change me')
    colour = models.CharField(max_length=25, default='bg-primary')
    
    def __str__(self):
        return self.name

class Area(models.Model):
    school = models.ForeignKey('school', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.school.name + " " + self.name   

class Reading(models.Model):
    area = models.ForeignKey('area', on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=200)
    amount = models.IntegerField()
    
    def __str__(self):
        return self.area.school.name + " " + self.area.name + " " + self.type + " reading"

