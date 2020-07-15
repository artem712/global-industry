from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Employee

# Create your views here.

def index(request):
    return render(request, 'inventory/index.html')

def dashboard(request):
	return render(request, 'inventory/dashboard.html')

def dash(request):
    return render(request, 'inventory/dashboard.html')	

def employee(request):
	Emps = Employee.objects.all()
	return render(request, 'inventory/dashboard/employee.html', { 'Emps': Emps })    

