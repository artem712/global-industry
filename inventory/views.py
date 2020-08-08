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
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def register(request):
	if request.method=="POST":
		username = request.POST['username']
		password = request.POST['password']
		name 	 = request.POST['name']
		if User.objects.filter(username=username).exists():
			messages.error(request,'Username is aldready taken')
			messages.info(request,'Try Another Username')
			return redirect('/register')

		user = User.objects.create_user(username=username, password=password, first_name=name)
		user.save() 
		messages.success(request,'Account created successfully for'==user)
		return redirect('/login')
	return render(request,'inventory/register.html')
	
def login(request):
	if request.method=="POST":
		username = request.POST['username']
		password = request.POST['password']

		user = auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request, user)
			messages.success(request,'{},  Welcome :)'.format(user))
			return redirect('/dashboard')
		else:
			messages.error(request,'Username or password incorrect')
		
	return render(request,'inventory/login.html')


def logoutUser(request):
	logout(request)
	return redirect('/')

def index(request):
    return render(request, 'inventory/index.html')

def dashboard(request):
	return render(request, 'inventory/dashboard.html')
	
# _____________________ For Employee _______________________________

def employee(request):
	Emps = Employee.objects.all()
	return render(request, 'inventory/employee.html', { 'Emps': Emps })   

def add_employee(request):
	form=EmployeeForm(request.POST or None, request.FILES or None)
	if request.method=="POST":
		form=EmployeeForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Employee Created.')
			return redirect('/employee')
		else:
			messages.error(request, 'Employee Not Created.')
			messages.error(request, form.errors)
	header = "Create Employee here" 
	return render(request,'inventory/add_common.html',{'form': form, 'header' : header })

def emp_edit(request, emp_id):
	emp = get_object_or_404(Employee, pk=emp_id)
	if request.method == "POST":
		form = EmployeeForm(request.POST, instance=emp)
		if form.is_valid():
			form.save()
			messages.success(request, '{} updated'.format(emp.name))
			return redirect('/employee')
		else:
			messages.error(request, '{} is not updated'.format(emp.name))
			messages.error(request, form.errors)
	else:
		form = EmployeeForm(instance=emp)
	header = "{} Details".format(emp)
	return render(request, 'inventory/add_common.html', {'form': form, 'header' : header })

def delete_employee(request, emp_id):
	emp = get_object_or_404(Employee, pk=emp_id)
	messages.success(request, '{} is deleted'.format(emp))
	emp.delete()
	return redirect('/employee')

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

			if(form.material.is_available(form.weight)):
				form.product.add_product(form.weight)
				form.material.reduce(form.weight)
				try:
					raw_waste = Products.objects.get(name='raw_waste')
				except ObjectDoesNotExist:
					raw_waste = Products(name='raw_waste')

				w = ( form.weight / form.material.getmake()) - form.weight 
				raw_waste.add_product(w)
				raw_waste.save()
				emp.add_bonus(form.product.get_wages() * form.weight)
				emp.save()
				form.save()
				messages.success(request, 'Work updated for {}'.format(emp))
				return redirect('/employee')
			else:
				messages.error(request, 'There is no such amount of raw materials to make this product.')
		messages.error(request, 'Work is Not updated for {}.'.format(emp))

	header = "Add work for {}".format(emp)
	form = WorkForm(initial={'emp': emp })
	return render(request, 'inventory/add_common.html', {'form' : form, 'header' : header })


# _____________________ For ProductS _______________________________


def product_details(request):
	pro = Products.objects.all()
	return render(request, 'inventory/product_details.html', { 'pro': pro })	

def add_product(request):
	form=ProductForm(request.POST or None, request.FILES or None)
	if request.method=="POST":
		form=ProductForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Product Created.')
			return redirect('/product_details')
		else:
			messages.error(request, 'Product not Created.')
			messages.error(request, form.errors)
	header = 'Create new Product'
	return render(request,'inventory/add_common.html',{'form': form, 'header' : header })

def edit_product(request, pro_id):
	pro = get_object_or_404(Products, pk=pro_id)
	if request.method == "POST":
		form = ProductForm(request.POST, instance=pro)
		if form.is_valid():
			form.save()
			messages.success(request, '{} updated.'.format(pro))
			return redirect('/product_details')
	else:
		form = ProductForm(instance=pro)
	header = "{} Details".format(pro) 
	return render(request, 'inventory/add_common.html', {'form': form, 'header' : header })


def delete_product(request, pro_id):
	pro = get_object_or_404(Products, pk=pro_id)
	messages.success(request, '{} is deleted'.format(pro))
	pro.delete()
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
	messages.success(request, 'Payed to {}'.format(emp))	
	return redirect('/salary_cal')

def pay_all(request):
	emp = Employee.objects.all()
	for e in emp :
		if e.isPaid == 0 :
			pay_now(request, e.id, True)
	messages.success(request, 'Payed All')
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
	cus = Customer.objects.all()
	return render(request, 'inventory/customer.html', { 'cus': cus })	

def add_customer(request):
	form=CustomerForm(request.POST or None, request.FILES or None)
	if request.method=="POST":
		form=CustomerForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Customer Created.')
			return redirect('/customer')
		else:
			messages.error(request, 'Customer not Created.')
			messages.error(request, form.errors)
	header = 'Create customer' 
	return render(request,'inventory/add_common.html',{'form': form, 'header' : header })

def cust_edit(request, cus_id):
	cus = get_object_or_404(Customer, pk=cus_id)
	if request.method == "POST":
		form = CustomerForm(request.POST, instance=cus)
		if form.is_valid():
			form.save()
			messages.success(request, '{} updated.'.format(cus))
			return redirect('/customer')
		else:
			messages.error(request, 'Customer is not updated.')
			messages.error(request, form.errors)
	else:
		form = CustomerForm(instance=cus)
	header = "{} views".format(cus)
	return render(request, 'inventory/add_common.html', {'form': form, 'header' : header })

def delete_customer(request, cus_id):
	cus = get_object_or_404(Customer, pk=cus_id)
	messages.success(request, '{} is deleted'.format(cus))
	cus.delete()
	return redirect('/customer')

# _____________________ For Orders _______________________________
			
def order_all(request):
	return render(request, 'inventory/order.html', {'order' : Orders.objects.all() })

def order_not_delivered(request):
	return render(request, 'inventory/order.html', {'order' : Orders.objects.filter(isDelivered=False) })

def order_delivered(request):
	return render(request, 'inventory/order.html', {'order' : Orders.objects.filter(isDelivered=True) })

def order_list(request, cus_id): # for particular customer 
	cus = get_object_or_404(Customer, pk=cus_id)
	order = Orders.objects.filter(cus=cus_id)
	return render(request, 'inventory/order.html', {'order' : order})

def order_details(request, ord_id): # particular order details 
	order = get_object_or_404(Orders, pk=ord_id)
	items = OrderItems.objects.filter(order=ord_id)
	return render(request, 'inventory/order_details.html', {'items' : items, 'order' : order })	

def order_now(request, cus_id):
	if request.method == 'POST':
		formset = OrderFormset(request.POST)
		if formset.is_valid() :
			cus 	= get_object_or_404(Customer, pk=cus_id)
			total 	= 0 
			order 	= Orders(cus=cus, total_amt=total, Odate=now())
			order.save() 
			for form in formset: 
				product = form.cleaned_data.get('product')
				weight 	= form.cleaned_data.get('weight')
				total  += ( product.cost * weight ) 
				items 	= OrderItems(order=order,product=product, weight=weight) 
				items.save()
			order.total_amt = total 
			order.save() 
			messages.success(request, 'Order Booked.')
			return redirect('/customer')
		else:
			messages.error(request, 'Order Canceled.'.format(sup))
			messages.error(request, formset.errors)
	else:
		formset = OrderFormset(request.GET or None)
	return render(request, 'inventory/order_now.html', { 'formset': formset })

def delivered(request, ord_id):
	order 			  = get_object_or_404(Orders, pk=ord_id)
	items 			  = OrderItems.objects.filter(order=order)
	for i in items :
		if(i.product.is_available(i.weight) == False):
			messages.error(request, '{} is Out of Stock!'.format(i.product.name))
			messages.error(request, 'Order cannot be deliver.')
			return redirect('/order_all')

	for i in items :
		i.product.reduce_product(i.weight)

	order.Ddate 	  = now()
	order.isDelivered = True
	order.save()
	messages.success(request, 'Order Completed.')
	return redirect('/order_all')


# _____________________ For Supplier _______________________________

def supplier(request):
	Sup = Supplier.objects.all()
	return render(request, 'inventory/supplier.html', { 'Sup': Sup })

def add_supplier(request):
	form=SupplierForm(request.POST or None, request.FILES or None)
	if request.method=="POST":
		form=SupplierForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Supplier Created.')
			return redirect('/supplier')
		else:
			messages.error(request, 'Supplier not Created.')
			messages.error(request, form.errors)
	header = 'Add Supplier'
	return render(request,'inventory/add_common.html',{'form': form, 'header' : header })

def sup_edit(request, sup_id):
	sup = get_object_or_404(Supplier, pk=sup_id)
	form = SupplierForm(instance=sup)
	if request.method == "POST":
		form = SupplierForm(request.POST, instance=sup)
		if form.is_valid():
			form.save()
			messages.success(request, '{} Modified.'.format(sup))
			return redirect('/supplier')
		else:
			messages.error(request, '{} not altered.'.format(sup))
			messages.error(request, form.errors)
	header = "Modify {}".format(sup)
	return render(request, 'inventory/add_common.html', {'form': form, 'header' : header })	

def delete_supplier(request, sup_id):
	sup = get_object_or_404(Supplier, pk=sup_id)
	name = sup.name
	sup.delete()
	messages.success(request, '{} deleted.'.format(name))
	return redirect('/supplier')		

def buy_material(request):
	form=MaterialsOrderForm(request.POST or None, request.FILES or None)
	if request.method=="POST":
		form=MaterialsOrderForm(request.POST)
		if form.is_valid():
			material = form.cleaned_data.get('material')
			weight 	 = form.cleaned_data.get('weight')
			rm = get_object_or_404(raw_materials, name=material)
			rm.update_weight(weight)
			rm.save() 
			form.save()
			messages.success(request, '{} is boughted.'.format(material))
			return redirect('/materials')
		else:
			messages.error(request, form.errors)
	header = 'Buy '
	return render(request,'inventory/add_common.html',{'form': form})



# _____________________ For Raw Materials _______________________________

def materials(request):
	mat = raw_materials.objects.all()
	return render(request, 'inventory/materials.html', { 'mat': mat })

def add_material(request):
	form=MaterialsForm(request.POST or None, request.FILES or None)
	if request.method=="POST":
		form=MaterialsForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Raw Material is Created.')
			return redirect('/materials')
		else:
			messages.error(request, 'Material is not created')
			messages.error(request,  form.errors)
	header = "Add New Raw Material" 
	return render(request,'inventory/add_common.html',{'form': form, 'header' : header })

def material_edit(request, mat_id):
	mat = get_object_or_404(raw_materials, pk=mat_id)
	if request.method == "POST":
		form = MaterialsForm(request.POST, instance=mat)
		if form.is_valid():
			form.save()
			messages.success(request, '{} is updated'.format(mat))
			return redirect('/materials')
		else:
			messages.error(request,  form.errors)
	form 	= MaterialsForm(instance=mat)
	header  = "Update {}".format(mat)   
	return render(request, 'inventory/add_common.html', {'form': form, 'header' : header })

def delete_material(request, mat_id):
	mat = get_object_or_404(raw_materials, pk=mat_id)
	messages.success(request, '{} is deleted'.format(mat))
	mat.delete()
	return redirect('/materials')