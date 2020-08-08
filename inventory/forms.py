
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

class EmployeeForm(forms.ModelForm):
	class Meta:
		model=Employee
		fields=('name','designation','address','phone','dob','doj','basicSalary','gender', 'lastSalary', 'bonus')

class CustomerForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=('name','address','phone')		

class WorkForm(forms.ModelForm):
	#emp = forms.IntegerField(widget=forms.HiddenInput())
	class Meta:
		model=Work
		#fields=('product', 'weight')
		exclude= ["emp"]

class ProductForm(forms.ModelForm):
	class Meta:
		model=Products
		fields=('name','cost','wages','weight')

class OrderForm(forms.ModelForm): 
	class Meta:
		model=Orders
		fields=('cus', 'product')

class SupplierForm(forms.ModelForm):
	def __init__(self,data=None,files=None,request=None,recipient_list=None,*args,**kwargs):
		super().__init__(data=data,files=files,request=request,*args,**kwargs)
		self.fields['name'].widget.attrs['placeholder']='name'
		self.fields['address'].widget.attrs['placeholder']='address'
		self.fields['phone'].widget.attrs['placeholder']='phone'
	class Meta:
		model=Supplier
		fields=('name','address','phone')
	
       		

class CreateUserForm(UserCreationForm):
	class Meta:
		model=User
		fields=['username','email','password1','password2']
