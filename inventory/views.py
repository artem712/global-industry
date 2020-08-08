from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.db.models import Q
from .models import *	
from .forms import *

# Create your views here.
def registerPage(request):

	form=CreateUserForm()

	if request.method=="POST":
		form=CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			user=form.cleaned_data.get('username')
			messages.success(request,'Account created successfully for'==user)
			return redirect('signup:login')

	return render(request,'signup/register.html',{'forms':form})
	
def loginPage(request):
	if request.method=="POST":
		username=request.POST.get('username')
		password=request.POST.get('password')

		user=authenticate(request,username=username,password=password)
		if user is not None:
			login(request)
			return redirect('inventory:dashboard')

		else:
			messages.info(request,'Username or password incorrect')

			
	return render(request,'signup/login.html')

def logoutUser(request):
	logout(request)
	return redirect('inventory:login')


def index(request):
    return render(request, 'inventory/index.html')

def dashboard(request):
	return render(request, 'inventory/dashboard.html')
	
# _____________________ For Employee _______________________________

def employee(request):
	Emps = Employee.objects.all()
	return render(request, 'inventory/employee.html', { 'Emps': Emps })    

def add_employee(request):
	if request.method=="POST":
		form=EmployeeForm(request.POST)

		if form.is_valid():
			form.save()
			return redirect('/employee')
	else:
		form=EmployeeForm()
		return render(request,'inventory/add_employee.html',{'form': form})


def emp_edit(request, emp_id):
	emp = get_object_or_404(Employee, pk=emp_id)
	if request.method == "POST":
		form = EmployeeForm(request.POST, instance=emp)
		if form.is_valid():
			form.save()
			return redirect('/employee')
	else:
		form = EmployeeForm(instance=emp)
		return render(request, 'inventory/edit_emp.html', {'form': form, 'emp' : emp})


def delete_employee(request, emp_id):
	Employee.objects.filter(id=emp_id).delete()
	Emps = Employee.objects.all()
	return render(request, 'inventory/employee.html', { 'Emps' : Emps } )

def view_works(request, emp_id):
	emp = get_object_or_404(Employee, pk=emp_id)
	wk = Work.objects.filter(emp=emp_id)
	return render(request, 'inventory/view_works.html', { 'wk' : wk, 'emp' : emp })

def add_work(request, emp_id):
	emp = get_object_or_404(Employee, pk=emp_id)

	if request.method=="POST":
		form=WorkForm(request.POST)
		if form.is_valid():
			form = form.save(commit=False)
			form.emp = emp 
			form.product.add_product(form.weight)
			emp.add_bonus( form.product.get_wages() * form.weight)
			emp.save()
			form.save()
			return redirect('/employee')
	else:
		form = WorkForm(initial={'emp': emp })
		return render(request, 'inventory/add_work.html', {'form' : form, 'emp' : emp })


# _____________________ For ProductS _______________________________


def product_details(request):
	pro = Products.objects.all()
	return render(request, 'inventory/product_details.html', { 'pro': pro })	

def add_product(request):
	if request.method=="POST":
		form=ProductForm(request.POST)

		if form.is_valid():
			form.save()
		return redirect('/product_details')
	else:
		form=ProductForm()
		return render(request,'inventory/add_product.html',{'form': form})

def edit_product(request, pro_id):
	pro = get_object_or_404(Products, pk=pro_id)
	if request.method == "POST":
		form = ProductForm(request.POST, instance=pro)
		if form.is_valid():
			form.save()
			return redirect('/product_details')
	else:
		form = ProductForm(instance=pro)
		return render(request, 'inventory/edit_product.html', {'form': form, 'pro' : pro})


def delete_product(request, pro_id):
	Products.objects.filter(id=pro_id).delete()
	return redirect('/product_details')


# _____________________ For Salary _______________________________

def get_total():
	emp = Employee.objects.all()
	for e in emp :
		e.total = e.bonus + e.basicSalary 
		e.save()

def salary_details(request, emp_id):
	emp = get_object_or_404(Employee, pk=emp_id)
	sal = Salary.objects.filter(emp=emp)
	return render(request, 'inventory/salary_details.html', {'sal': sal, 'emp' : emp } )

def pay_now(request, emp_id, isall=False):
	emp = get_object_or_404(Employee, pk=emp_id)
	s 	= Salary(emp=emp, basicSalary=emp.basicSalary, bonus=emp.bonus, total=emp.total)
	s.save()
	emp.isPaid 	= True
	emp.bonus 	= 0  
	emp.lastSalary = now()
	emp.save() 

	if isall :
		return  
	return redirect('/salary_cal')

def pay_all(request):
	emp = Employee.objects.all()
	for e in emp :
		if e.isPaid == 0 :
			pay_now(request, e.id, True)
	return redirect('/salary_cal')

def salary_cal(request):
	get_total() 	
	emp = Employee.objects.all()
	for e in emp : 
		if ( now() - e.lastSalary > timedelta(days=7) ) :
			e.isPaid = False 
			e.save()  

	return render(request, 'inventory/salary_cal.html', {'emp' : emp })


# _____________________ For customer _______________________________


def customer(request):
	Cust = Customer.objects.all()
	return render(request, 'inventory/customer.html', { 'Cust': Cust })	

def add_customer(request):
	if request.method=="POST":
		form=CustomerForm(request.POST)

		if form.is_valid():
			form.save()
			return redirect('/customer')
	else:
		form=CustomerForm()
		return render(request,'inventory/add_customer.html',{'form': form})

def cust_edit(request, cus_id):
	cus = get_object_or_404(Customer, pk=cus_id)
	if request.method == "POST":
		form = CustomerForm(request.POST, instance=cus)
		if form.is_valid():
			form.save()
			return redirect('/customer')
	else:
		form = CustomerForm(instance=cus)
		return render(request, 'inventory/edit_cust.html', {'form': form, 'cus' : cus})


def delete_customer(request, cus_id):
	Customer.objects.filter(id=cus_id).delete()
	Cus = Customer.objects.all()
	return render(request, 'inventory/customer.html', { 'Cus' : Cus } )

	
				

def new_order(request, cus_id):
	cus = get_object_or_404(Customer, pk=cus_id)
	orders = Orders.objects.filter(cus=cus_id)

	if request.method=="POST":
		form=OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/dashboard')
	else:
		form = OrderForm()
		return render(request, 'inventory/order_info.html', {'form' : form, 'orders' : orders, 'cus' : cus })


# _____________________ For Supplier _______________________________

def supplier(request):
	Sup = Supplier.objects.all()
	return render(request, 'inventory/supplier.html', { 'Sup': Sup })

def add_supplier(request):
	if request.method=="POST":
		form=SupplierForm(request.POST)

		if form.is_valid():
			form.save()
			return redirect('/supplier')
	else:
		form=SupplierForm()
		return render(request,'inventory/add_supplier.html',{'form': form})

def sup_edit(request, sup_id):
	emp = get_object_or_404(Supplier, pk=sup_id)
	if request.method == "POST":
		form = SupplierForm(request.POST, instance=emp)
		if form.is_valid():
			form.save()
			return redirect('/supplier')
	else:
		form = SupplierForm(instance=emp)
		return render(request, 'inventory/edit_sup.html', {'form': form})	

def delete_supplier(request, sup_id):
	Supplier.objects.filter(id=sup_id).delete()
	Sup = Supplier.objects.all()
	return render(request, 'inventory/supplier.html', { 'Sup' : Sup } )			



def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user= auth.authenticate(username=username,password=password)
        if user is not None:
        	auth.login(request, user)
        	return render(request,'inventory/dashboard.html')
        else:
            return render(request,'inventory/register.html')	
    else:
      return render(request,'inventory/login.html')

