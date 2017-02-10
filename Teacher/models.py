from django.db import models
import datetime

class GoodDeed(models.Model):
	cost = models.IntegerField()
	name = models.CharField(max_length=1000)
	id_num = models.IntegerField()
	defined = models.BooleanField()	
	created = models.BooleanField()


#this is mapped to which button the student presses -> map to ID_num -> display using context on teacher's screen
class Request(models.Model):
	custom_input = models.CharField(max_length=1500, default="")
	g_deed = models.IntegerField(default=0)
	points = models.IntegerField(default=0)
	requester_id = models.IntegerField(default=0)
	time_created = models.DateTimeField(auto_now_add=True)
	updated = models.BooleanField(default=False)
	identifier = models.CharField(max_length=500, default="")

class SpendRequest(models.Model):
	rewardname = models.CharField(max_length=500, default="")
	number = models.IntegerField(default=0)
	username = models.CharField(max_length=500, default="")
	studentname = models.CharField(max_length=500, default="")

	spender = models.CharField(max_length=500, default="")


class Reward(models.Model):
	cost = models.IntegerField()
	name = models.CharField(max_length=1000)
	id_num = models.IntegerField(default=0)


#, auto_add=False
#, default=datetime.datetime(1, 1, 1, 01, 01, 01)

# Create your models here.
