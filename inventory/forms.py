from django import forms
from .models import *

class EmployeeForm(forms.ModelForm):
	class Meta:
		model=Employee
		fields=('name','designation','address','phone','dob','doj','salary','gender')

class WorkForm(forms.ModelForm):
	class Meta:
		model=Work
		fields=('emp', 'product', 'weight')