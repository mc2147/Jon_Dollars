from django.db import models
from django.contrib.auth.models import User
from django.http import HttpResponse

class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	points = models.IntegerField()
	inventory = []
	inventory_backup = models.CharField(max_length=1000,default="")
	teacher_id = models.CharField(max_length=100, default=0)

class Teacher(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	teacher_id = models.CharField(max_length=100, default="")
	inbox = []
	inbox_backup = models.CharField(max_length=1000,default="")	
	spendbox = []
	spendbox_backup = models.CharField(max_length=1000,default="")
	students = models.ManyToManyField("Student")

class Team(models.Model):
	name = models.CharField(max_length=500,default="")
	points = models.IntegerField(default=0)
	members = models.ManyToManyField("Student")

class Classroom(models.Model):
	class_num = models.IntegerField(default=0)
	name = models.CharField(max_length=500,default="")
	students = models.ManyToManyField("Student")
