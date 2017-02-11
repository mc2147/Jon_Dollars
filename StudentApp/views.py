import datetime
from django.shortcuts import render
from .models import Student, Teacher
from django.contrib.auth.models import User
from Teacher.models import GoodDeed, Request, SpendRequest, Reward
from django.template import Context, Template
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def teacher_check(user):
	return Teacher.objects.filter(user=user).exists()

def FirstPage(request):
	context = {}
	reg_user = request.user.username
	if(request.POST.get("s-login")):
		u_name = request.REQUEST.get("username")
		p_word = request.REQUEST.get("password")
		if User.objects.filter(username=u_name).exists():
			user = User.objects.get(username=u_name)
			user.is_active = True
			user.save()		
		auth = authenticate(username=u_name, password=p_word)
		if auth:
			user.save()			
			if teacher_check(user) == False:
				login(request, auth)
				print("STUDENT LOGIN SUCCESS")
				print(request.user.username)
				return HttpResponseRedirect('/student/home')

	if (request.POST.get("t-login")):
		u_name = request.REQUEST.get("username")
		p_word = request.REQUEST.get("password")
		print(u_name)
		print(p_word)		
		if User.objects.filter(username=u_name).exists():
			user = User.objects.get(username=u_name)
			user.is_active = True
			user.save()
		auth = authenticate(username=u_name, password=p_word)
		if auth:
			if teacher_check(user):
				login(request, auth)
				user.save()
				print("TEACHER LOGIN SUCCESS")
				print(request.user.username)
				return HttpResponseRedirect('/teacher/home')

	return render(request, "login.html")


@login_required(login_url='http://127.0.0.1:8000/login')
def StudentHome(request):
	if request.GET.get("logout"):
		logout(request)
		return FirstPage(request)#HttpResponseRedirect('http://127.0.0.1:8000/login')
	user = request.user
	student = Student.objects.get(user=user)
	points = student.points
	dollars = (points - (points % 10))/10
	until = 10 - (points % 10)

	context = {}
	context["Name"] = user.first_name + " " + user.last_name
	context["Dollars"] = dollars
	context["Points"] = points
	context["Until"] = until

	return render(request, "StudentHome.html", context)

def Team(request):
	return render(request, "Team.html")


@login_required(login_url='http://127.0.0.1:8000/login')
def Shop(request):
	if request.GET.get("logout"):
		logout(request)
		return FirstPage(request)
	student_user = request.user 
	username = student_user.username
	student = Student.objects.get(user=student_user)
	student_name = student_user.first_name + " " + student_user.last_name
	dollars = student.points/10	
	available_rewards = Reward.objects.all()
	context = {}
	context["RewardsList1"] = []
	context["RewardsList2"] = []
	for i in available_rewards:
		display = []
		display.append(i.name) #0 is name
		display.append(i.cost) #1 is cost
		display.append(i.pk) #2 is pk ID
		if len(context["RewardsList1"]) < 5:
			context["RewardsList1"].append(display)
		elif len(context["RewardsList1"]) == 5:
			context["RewardsList2"].append(display) 
	
	print(available_rewards)
	print(context["RewardsList2"])			

	context["PointsAvailable"] = student.points
	context["DollarsAvailable"] = student.points

	for i in available_rewards:
		print(i.pk)
		if(request.GET.get('buy' + str(i.pk))):
			print("this is reward number " + str(i))
			item = i
			name_ = item.name
			cost_ = item.cost
			if student.points < cost_:
				context["NotEnough"] = "You do not have enough points to buy this!"
			else:
				new_spend = SpendRequest(rewardname=name_,username=username,number=0,studentname=student_name)
				new_spend.save()
				student.points = student.points - cost_
				student.inventory.append(name_)
				student.save()
				return HttpResponseRedirect('/student/shop')
				print(student.inventory)

	return render(request, "Shop.html", context)


@login_required(login_url='http://127.0.0.1:8000/login')
def Inventory(request):
	if request.GET.get("logout"):
		logout(request)
		return FirstPage(request)
	current_user = request.user
	context = {}
	context["List"] = []
	student = Student.objects.get(user=current_user)
	s = SpendRequest.objects.filter(username=current_user.username)
	inventory = []
	for i in s:
		print(i.rewardname)
		row = []
		row.append(i.pk) #0 is ID
		row.append(i.rewardname) #1 is reward name
		row.append("S" + str(i.pk)) #2 is button name
		context["List"].append(row)
		
	return render(request, "Inventory.html", context)


@login_required(login_url='http://127.0.0.1:8000/login')
def PointRequest(request):
	if request.GET.get("logout"):
		logout(request)
		return FirstPage(request)
	studentuser = request.user
	student = Student.objects.get(user = studentuser)
	studentpoints = student.points
	dollars = (studentpoints - (studentpoints % 10))/10

	context = {
		"empty_error": "",
		"Points": studentpoints,
		"Dollars": dollars,
	}

	if(request.GET.get("custom-request-btn")):
		c_input = request.REQUEST.get("custom")
		n_points = request.REQUEST.get("num_points")
		if c_input != "":
			new_request = Request(custom_input=c_input, points=n_points, requester_id=studentuser.username,time_created=datetime.datetime.now())
			new_request.identifier = str(new_request.time_created)
			new_request.save()
		if c_input == "":
			print("empty case test")
			error = "You need to input a custom request!"
			context = {
				"empty_error": error,
			}
	GDs = GoodDeed.objects.all()	
	def UpdateContext():
		context["Deeds1"] = []
		context["Deeds2"] = []
		for i in GDs:
			if i.defined == True:
				GDList = []
				GDList.append(i.name) #0 is name
				GDList.append(i.cost) #1 is cost
				GDList.append(i.id_num) #2 is identifier
				if len(context["Deeds1"]) < 5:
					context["Deeds1"].append(GDList)
				else:
					context["Deeds2"].append(GDList)
		

		print(context["Deeds1"])
		print(context["Deeds2"])
	
	UpdateContext()

	def buttons():
		for i in context["Deeds1"]:
			index = i[2] 
			if (request.GET.get('req_' + str(index))):
				student = Student.objects.get(user=studentuser)
				s_username = student.user.username
				deed = GoodDeed.objects.get(id_num=index)
				new_request = Request(custom_input="", g_deed=deed.id_num, points=deed.cost, requester_id=s_username,time_created=datetime.datetime.now())#, updated=False)
				new_request.identifier = str(new_request.time_created)
				new_request.save()
				deed_name = deed.name
				print(deed.name + " requested")
		for i in context["Deeds2"]:
			index = i[2]
			if (request.GET.get('req_' + str(index))):
				student = Student.objects.get(user=studentuser)
				s_username = student.user.username
				deed = GoodDeed.objects.get(id_num=index)
				new_request = Request(custom_input="", g_deed=deed.id_num, points=deed.cost, requester_id=s_username,time_created=datetime.datetime.now())#, updated=False)
				new_request.identifier = str(new_request.time_created)
				new_request.save()
				deed_name = deed.name
				print(deed.name + " requested")
	buttons()
	return render(request, "PointRequest.html", context)


@login_required(login_url='http://127.0.0.1:8000/login')
def StudentSettings(request):
	if request.GET.get("logout"):
		logout(request)
		return FirstPage(request)
	user = request.user
	username=request.user.username
	pword = user.password
	if request.GET.get("usernamechange"):
		p_1 = request.REQUEST.get("password")
		p_2 = request.REQUEST.get("password_2")
		check_1 = (user.check_password(p_1))
		check_2 = (user.check_password(p_2))
		if check_1 and check_2:
			print("test")		
	if request.GET.get("passwordchange"):
		p_1 = request.REQUEST.get("password")
		p_2 = request.REQUEST.get("password_2")
		check_1 = (user.check_password(p_1))
		check_2 = (user.check_password(p_2))
		if check_1 and check_2:
			print("passwords match and are correct")
			new_username = request.REQUEST.get("newusername")
			new_password = request.REQUEST.get("newpassword")
			if new_username != "":
				username = request.REQUEST.get("newusername")
				user.save()
			if new_password != "":
				user.set_password(request.REQUEST.get("newpassword"))
				user.save()
	return render(request, "StudentSettings.html")

