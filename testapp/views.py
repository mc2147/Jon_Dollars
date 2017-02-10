from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def Test_1(request):
	user = request.user
	username = user.username
	context = {}
	context["user"] = user
	context["username"] = username
	context["user_list"] = []

	x = User.objects.all()
	for i in x:
		context["user_list"].append(i.username)
	print(user)

	return render(request, "Test.html", context)

def Test_Login(request):

	return render(request, "Test_2.html")


def Login(request):
	user = request.user
	print(user.username)
	context = {}
	if(request.GET.get("logout")):
		logout(request)
		print("LOGGED OUT")
		print(request.user.username)

	if(request.GET.get("s-login")):
		u_name = request.REQUEST.get("username")
		p_word = request.REQUEST.get("password")		
		auth = authenticate(username=u_name, password=p_word)

		print("THIS IS AUTH")
		print(auth)
		
		if auth:
			print("is_authenticated?")
			print(user.is_authenticated())
			user.save()			
			login(request, auth)
			print("LOGIN SUCCESS")
			print(request.user.username)
	
	if (request.GET.get("t-login")):
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
			login(request, auth)
			print(request.user.username)

	return render(request, "login.html", context)

def Check_Login(request):
	user = request.user
	username = user.username
	context = {}
	context["user"] = user
	context["username"] = username
	context["user_list"] = []

	x = User.objects.all()
	for i in x:
		row = []
		a = i.is_authenticated()
		row.append(i.username)
		row.append(a)
		context["user_list"].append(row)

	print(user)
	if(request.GET.get("login")):
		u_name = request.REQUEST.get("username")
		p_word = request.REQUEST.get("password")		
		#if User.objects.filter(username=u_name).exists():
		#	user = User.objects.get(username=u_name)
		#	user.is_active = True
		#	user.email = "test@gmail.com"
		#	user.save()
		auth = authenticate(username=u_name, password=p_word)
		print("THIS IS AUTH")
		print(auth)		
		if auth:
			print("is_authenticated?")
			print(user.is_authenticated())
			#user.save()			
			login(request, auth)
			print("LOGIN SUCCESS")
			print(request.user.username)
			#request.session.save()
			#return HttpResponseRedirect("student/home")	
	if(request.GET.get("logout")):
		logout(request)
	#Check: login function, authenticate function, logout, login_required

	return render(request, "check_login.html", context)

@login_required()
def Login_Required(request):

	return render(request, "LoginRequired.html")