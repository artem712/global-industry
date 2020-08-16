from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from tenants.models import Client, Domain

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		name 	 = request.POST['name']

		if username.isspace() == True :
			messages.error(request,'username must not conatain space')
			messages.info(request,'Try Another Username')
			return redirect('home:register')

		if User.objects.filter(username=username).exists() :
			messages.error(request,'Username is aldready taken')
			messages.info(request,'Try Another Username')
			return redirect('home:register')

		user = User.objects.create_user(username=username, password=password, first_name=name)
		user.save() 

		tenant = Client.objects.create(user=user, schema_name= user.username)
		tenant.save()
		domain = Domain()
		domain.domain = tenant.schema_name + ".global.localhost"
		domain.tenant = tenant 
		domain.is_primary = True
		domain.save()

		messages.success(request,'Account created successfully for {}'.format(name))
		return redirect('home:login')
	return render(request,'register.html')
	
def login(request):
	if request.method=="POST":
		username = request.POST['username']
		password = request.POST['password']

		user = auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request, user)
			messages.success(request,'{},  Welcome :)'.format(user))
			url = "http://" + username + ".global.localhost:8000/welcome/"
			return redirect(url)
		else:
			messages.error(request,'Username or password incorrect')
		
	return render(request,'login.html')


def logoutUser(request):
	logout(request)
	return redirect('home:index')