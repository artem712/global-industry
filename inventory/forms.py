from django import forms
from .models import *

class EmployeeForm(forms.ModelForm):
	class Meta:
		model=Employee
		fields=('name','designation','address','phone','dob','doj','salary','gender')