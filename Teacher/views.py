from django.shortcuts import render
from django.contrib.auth.models import User, Group
from StudentApp.models import Student, Teacher
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import GoodDeed, Request, SpendRequest, Reward
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout


def teacher_check(user):
	return Teacher.objects.filter(user=user).exists()

# Create your views here.
@user_passes_test(teacher_check)
def TeacherHome(request):
	if request.GET.get("logout"):
		logout(request)
		return HttpResponseRedirect('http://127.0.0.1:8000/login')

	request.session['inbox'] = {}
	t_inbox = request.session['inbox']
	print("Teacher Inbox Keys:")
	print(request.session['inbox'].keys())
	request.session['test'] = {1:"a", 2:"b", 3:"c", 4:"d"}	
	x = request.session.get('test')
	context = {}
	user = request.user
	print("this is user")
	print(user)
	
	context['Name'] = user.first_name
	print(user.first_name)
	name_list = []
	def createcontext():	
		n = Student.objects.count()
		a = Student.objects.all()
		for i in range(n):
			student_info = []
			student_info.append(a[i].user.first_name + " " + a[i].user.last_name) #0 is name
			student_info.append(a[i].points) #1 is points
			student_info.append(a[i].user.username) #2 is username
			name_list.append(student_info)
			context["names"] = name_list
			context["error"] = ""
	
	createcontext()

	def updatecontext():
		n = Student.objects.count()
		a = Student.objects.all()
		for i in a:
			student_info = []
			student_info.append(i.user.first_name + " " + i.user.last_name) #0 is name
			student_info.append(i.points) #1 is points
			student_info.append(i.user.username) #2 is username
			if student_info not in name_list:
				name_list.append(student_info)
				context["names"] = name_list
			
	
	for x in context.keys():
		print(x)
		print(context[x])
	if(request.GET.get('add_student_btn')):
		f_name = request.REQUEST.get("firstname")
		l_name = request.REQUEST.get("lastname")
		d_password = request.REQUEST.get("defaultpassword")
		student_id = request.REQUEST.get("ID")
		points = request.REQUEST.get("points")
		if User.objects.filter(username=student_id).exists():
			context["error"] = "This username is taken"
		else:
			new_user = User.objects.create_user(username=student_id, first_name=f_name, last_name=l_name, password=d_password)
			new_student = Student(user=new_user)
			new_student.points = points
			print(request.user.username)
			print(new_student.points)			
			teacher_id = request.user.username
			#new_student.teacher_id = teacher_id
			new_student.save()
			updatecontext()
			a = Student.objects.count()
			print(a)

	if(request.GET.get("edit_btn")):
		edit_username = request.REQUEST.get("select")
		points_user = User.objects.get(username=edit_username)
		points_student = Student.objects.get(user = points_user)
		if(edit_username):
			if request.REQUEST.get("cust_val") != "":
				newpoints = request.REQUEST.get("cust_val")
				points_student.points = newpoints
				points_user.save()				
				points_student.save()
			if request.REQUEST.get("new_fname") != "":
				newfname = request.REQUEST.get("new_fname")
				points_user.first_name = newfname
				points_user.save()				
				points_student.save()
			if request.REQUEST.get("new_lname") != "":
				newlname = request.REQUEST.get("new_lname")
				points_user.last_name = newlname
				points_user.save()				
				points_student.save()
		return HttpResponseRedirect("/teacher/home")

	if(request.GET.get("delete_btn")):
		del_username = request.REQUEST.get("select")
		del_user = User.objects.get(username=del_username)
		del_student = Student.objects.get(user = del_user)
		del_student.delete()
		return HttpResponseRedirect("/teacher/home")


	if(request.GET.get("add_point_btn")):

		points_id = request.REQUEST.get('id_for_points')
		print("test begins here")
		points_user = User.objects.get(username=440131)
		points_student = Student.objects.get(user=points_user)
		print(points_student.points)
		points_student.points = points_student.points + 1 
		points_student.save()
		print(points_student.points)

	if(request.GET.get("remove_point_btn")):

		points_id = request.REQUEST.get('id_for_points')
		print("test begins here")
		#print(points_id) #<- works
		points_user = User.objects.get(username=440131)
		#print(points_user.first_name)
		points_student = Student.objects.get(user=points_user)
		print(points_student.points)
		points_student.points = points_student.points - 1
		points_student.save()
		print(points_student.points)


	return render(request, "TeacherHome.html", context)

@user_passes_test(teacher_check)
def GoodDeeds(request):
	if request.GET.get("logout"):
		logout(request)
		return HttpResponseRedirect('http://127.0.0.1:8000/login')
		
	print(GoodDeed.objects.count())
	for i in GoodDeed.objects.all():
		print(i.name)
	default_dict = {
			"GD_1" : "Enter Deed Here",
			"GD_2" : "Enter Deed Here",
			"GD_3" : "Enter Deed Here",
			"GD_4" : "Enter Deed Here",
			"GD_5" : "Enter Deed Here",
			"GD_6" : "Enter Deed Here",
			"GD_7" : "Enter Deed Here",
			"GD_8" : "Enter Deed Here",
			"GD_9" : "Enter Deed Here",
			"GD_10" : "Enter Deed Here",

			"P_1" : 0,
			"P_2" : 0,
			"P_3" : 0,
			"P_4" : 0,
			"P_5" : 0,
			"P_6" : 0,
			"P_7" : 0,
			"P_8" : 0,
			"P_9" : 0,
			"P_10" : 0,
			}

	def UpdateContext():
		output = default_dict
		for index in range(1, 11):
			GD_tag = "GD_" + str(index)
			P_tag = "P_" + str(index)	
			if (GoodDeed.objects.filter(id_num=index).exists()):
				a = GoodDeed.objects.get(id_num=index)
				if a.defined == True:
					output[GD_tag] = a.name
					output[P_tag] = a.cost
				if a.defined == False:
					output[GD_tag] = "Enter Deed Here" 
					output[P_tag] = 0
			else:
				new = GoodDeed()
				new.cost = 0
				new.id_num = index
				new.created = True
				new.defined = False
				new.name = "Good Deed " + str(index)	
				new.save()				
				output[GD_tag] = "Enter Deed Here"
				output[P_tag] = 0
		return output


	def buttons():
		if(request.GET.get('enter-deed-btn')):
			cost_ = request.REQUEST.get("value")
			name_ = request.REQUEST.get("gdname")
			for i in range(1, 11):
				gd_check = GoodDeed.objects.get(id_num=i)
				if gd_check.defined == False:
					gd_check.defined = True
					gd_check.cost = cost_
					gd_check.name = name_
					gd_check.save()
					UpdateContext()
					break					
				if gd_check.defined == True and i == 10:
					context["TooMany"] = "You have too many good deeds"
		if(request.POST.get("gdedit")):
			check_list = request.POST.getlist("gd")
			new_name = request.POST.get("editname")
			new_points = request.POST.get("editpoint")
			for i in check_list:
				if (GoodDeed.objects.filter(id_num=i).exists()):
					edit_gd = GoodDeed.objects.get(id_num=i)
					edit_gd.name = new_name
					edit_gd.cost = new_points
					edit_gd.defined = True
					edit_gd.save()
					UpdateContext()
				else:
					new_gd = GoodDeed()
					new_gd.name = new_name
					new_gd.id_num = i
					new_gd.cost = new_points
					new_gd.defined = True
					new_gd.save()
					UpdateContext()
		if(request.POST.get("gddelete")):
			check_list = request.POST.getlist("gd")
			for i in check_list:
				if (GoodDeed.objects.filter(id_num=i).exists()):
					del_gd = GoodDeed.objects.get(id_num=i)
					del_gd.delete()		
					UpdateContext()
	context = UpdateContext()
	buttons()
	if(request.GET.get('delete-deed-btn')):
		GoodDeed.objects.all().delete()
		UpdateContext()
	return render(request, "GoodDeeds.html", context)

@user_passes_test(teacher_check)
def Items(request):
	if request.GET.get("logout"):
		logout(request)
		return HttpResponseRedirect('http://127.0.0.1:8000/login')
	context = {}
	context["RewardsList"] = []
	def maxrewards():
		x = Reward.objects.count()
		return (x >= 10)

	if(request.POST.get("editrewards")):		
		check_list = request.POST.getlist("R")	
		for i in check_list:
			to_edit = Reward.objects.get(pk=i)
			to_edit.name = request.REQUEST.get("nreward")			
			to_edit.cost = request.REQUEST.get("npoint")
			to_edit.save()
	if(request.POST.get("delete")):
		del_list = request.POST.getlist("R")
		for i in del_list:
			to_delete = Reward.objects.get(pk=i)
			to_delete.delete()
	
	if(request.POST.get("addR")):
		name = request.REQUEST.get("Name")
		cost = request.REQUEST.get("Cost")
		if name != "" and cost != "":
			new_reward = Reward(name=name, cost=cost, id_num=0)
			new_reward.save()
	if(request.POST.get("clear")):
		Reward.objects.all().delete()
		context["RewardsList"] = []
	for i in Reward.objects.all():
		reward = []
		reward.append(i.name) #0 is name
		reward.append(i.cost) #1 is cost
		reward.append(i.pk) #2 is django ID
		context["RewardsList"].append(reward)

	return render(request, "Items.html", context)

@user_passes_test(teacher_check)
def TeacherSettings(request):
	if request.GET.get("logout"):
		logout(request)
		return HttpResponseRedirect('http://127.0.0.1:8000/login')
	print(request.user.username)
	user = request.user
	test_user = User.objects.get(username=440131)
	test_username = test_user.username
	pword = test_user.password

	if request.POST.get("usernamechange"):
		p_1 = request.POST.get("password")
		p_2 = request.POST.get("password_2")
		check_1 = (user.check_password(p_1))
		check_2 = (user.check_password(p_2))
		new_username = request.POST.get("newusername")
		print(new_username)			
		if check_1 and check_2:
			print("test")		
			if new_username != "":
				user.username = new_username
				user.save()
			
	if request.POST.get("passwordchange"):
		p_1 = request.POST.get("password")
		p_2 = request.POST.get("password_2")
		check_1 = (user.check_password(p_1))
		check_2 = (user.check_password(p_2))
		if check_1 and check_2:
			print("passwords match and are correct")
			new_password = request.POST.get("newpassword")
			if new_password != "":
				user.set_password(new_password)
				user.save()

	return render(request, "TeacherSettings.html")

@user_passes_test(teacher_check)
def Requests(request):
	if request.GET.get("logout"):
		logout(request)
		return HttpResponseRedirect('http://127.0.0.1:8000/login')
	#inbox = request.session['inbox']
	#keys = sorted(inbox.keys(), reverse=True)

	requests = Request.objects.all()
	identifiers = []
	for i in requests:
		identifiers.append(i.identifier)
	keys = sorted(identifiers, reverse=True)

	context = {}
	context["RequestKeys"] = []
	context["Names"] = []
	context["Deeds"] = []
	context["Points"] = []
	context["Times"] = []
	context["IDs"] = []
	context["TableRows"] = []

	def create_context(i, name, points, deed, time):
			#n = keys.index(i)
			row = []
			row.append(i + 1)
			row.append(name)
			row.append(points)
			row.append(deed)
			row.append("A" + str(i))
			row.append("D" + str(i))
			row.append(time)
			context["TableRows"].append(row)

	def update_context(i):
		for row in context["TableRows"]:
			if row[0] == i + 1:
				context["TableRows"].remove(row)
			if row[0] > i + 1:
				row[0] = row[0] - 1

	def check_btns(i, student, n_points):
		if request.POST.get("A" + str(i)):
			student.points = student.points + n_points
			student.save()
			print(student.user.first_name + "has " + str(student.points) + " points")
			#3 LEVELS OF EDITING
			#MODEL(STUDENT OBJECT)
			x = Request.objects.get(identifier=keys[i])
			x.delete()
			#REQUEST SESSION (TEACHER INBOX)
			#request.session['inbox'].pop(keys[i])
			#request.session.save()
			#CONTEXT (FRONT END HTML)
			update_context(i)
			print(context["TableRows"])
			return HttpResponseRedirect('/teacher/requests')
		if request.POST.get("D" + str(i)):
			x = Request.objects.get(identifier=keys[i])
			x.delete()
			#request.session['inbox'].pop(keys[i])
			#request.session.save()
			update_context(i)
			print(context["TableRows"])							
			return render(request, "TeacherRequests.html", context)

	#for every request in inbox, a new list is created to make a row
	for i in range(len(keys)):
		x = Request.objects.get(identifier=keys[i])
		r_username = x.requester_id
		r_user = User.objects.get(username=r_username)
		name = r_user.first_name + " " + r_user.last_name
		n_points = x.points
		deed = x.g_deed
		student = Student.objects.get(user=r_user)
		time = keys[i]


		#n_points = int(inbox[keys[i]]["Points"])
		#r_username = inbox[keys[i]]["requester_id"]
		#r_user = User.objects.get(username=r_username)
		#deed = inbox[keys[i]]["Deed"]
		print(n_points)
		check_btns(i, student, n_points)
		create_context(i, name, n_points, deed, time)

	if request.GET.get('update'):
		return HttpResponseRedirect('/teacher/requests')
	
	if request.GET.get("delete"):
		Request.objects.all().delete()
		#request.session['inbox'] = {}
		#request.session.save()
		context["TableRows"] = []
		return render (request, "TeacherRequests.html", context)

	print(context["TableRows"])

	return render(request, "TeacherRequests.html", context)

@user_passes_test(teacher_check)
def SpendRequests(request):
	if request.GET.get("logout"):
		logout(request)
		return HttpResponseRedirect('http://127.0.0.1:8000/login')
	spend_inbox = []
	index_list = []
	x = SpendRequest.objects.all()
	def create_inbox():
		for index in range(len(x)):
			row = []
			row.append(index) #0 is index
			row.append(x[index].rewardname) #1 is reward name
			row.append(x[index].studentname) #2 is student name
			row.append(x[index].username) #3 is student username 
			spend_inbox.append(row)
			print(spend_inbox)
			index_list.append(index)

	def check_buttons():
		for i in index_list:
			if request.GET.get("S" + str(i)):
				
				student_user = User.objects.get(username=spend_inbox[i][3])
				student = Student.objects.get(user=student_user)
				student.inventory.remove(spend_inbox[i][1])
				student.save()

				spend_inbox.remove(spend_inbox[i])
				request.session.save()
				
				x[i].delete()				
				index_list.remove(index_list[i])				

				reindex(i)
				print("S" + str(i) + "input received")


	def reindex(index):
		for i in spend_inbox:
			if i[0] > index:
				i[0] = i[0] - 1
		for x in index_list:
			if x > index_list:
				x = x - 1

	create_inbox()
	check_buttons()

	context = {}
	
	context["TableRows"] = spend_inbox

	print(spend_inbox)
	
	if request.GET.get("update"):
		return render(request, "TeacherSpend.html", context)

	if request.POST.get("clear"):
		SpendRequest.objects.all().delete()
		spend_inbox = []
		request.session.save()
		context["TableRows"] = spend_inbox
		return render(request, "TeacherSpend.html", context)

	
	return render(request, "TeacherSpend.html", context)



