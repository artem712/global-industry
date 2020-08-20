from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm

class UserForm(UserChangeForm):
	class Meta:
		model=User
		fields=['username','email','first_name','last_name']
		labels={
		   'last_name':'phone no',
		   'first_name':'Organisation name'
		}
		widgets={
		'username':forms.TextInput(attrs={'class':'form-control',}),
		'email':forms.TextInput(attrs={'class':'form-control',}),
		'first_name':forms.TextInput(attrs={'class':'form-control',}),
		'last_name':forms.TextInput(attrs={'class':'form-control'}),
		}

class PasswordForm(PasswordChangeForm):
	class Meta:
		model=User
		fields=['old_password','new_password','new_password_confirmation',]
		widgets={
		'old_password':forms.TextInput(attrs={'class':'form-control',}),
		'new_password':forms.TextInput(attrs={'class':'form-control',}),
		'new_password_confirmation':forms.TextInput(attrs={'class':'form-control'}),
		}

