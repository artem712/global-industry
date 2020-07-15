from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# Create your views here.

def index(request):
    return render(request, 'inventory/index.html')

def dashboard(request):
	return render(request, 'inventory/base.html')

def dash(request):
    return render(request, 'inventory/dashboard.html')	

