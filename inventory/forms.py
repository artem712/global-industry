from django import forms
from .models import *

class EmployeeForm(forms.ModelForm):
	class Meta:
		model=Employee
		fields=('name','designation','address','phone','dob','doj','basicSalary','gender')

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
    class Meta:
        model=Supplier
        fields=('name','address','phone')		

