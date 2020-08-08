from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import formset_factory, modelformset_factory
from .models import *

TOTAL_FORM_COUNT = 'TOTAL_FORMS'
INITIAL_FORM_COUNT = 'INITIAL_FORMS'
MIN_NUM_FORM_COUNT = 'MIN_NUM_FORMS'
MAX_NUM_FORM_COUNT = 'MAX_NUM_FORMS'
ORDERING_FIELD_NAME = 'ORDER'
DELETION_FIELD_NAME = 'DELETE'

# default minimum number of forms in a formset
DEFAULT_MIN_NUM = 0

# default maximum number of forms in a formset, to prevent memory exhaustion
DEFAULT_MAX_NUM = 1000

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
		fields=('cus',)

class OrderNowForm(forms.Form):
	product = forms.ModelChoiceField(queryset=Products.objects.all(),  empty_label="Select the Product", required=True)
	weight  = forms.DecimalField(max_digits=10, decimal_places=2 ,required=True, 
		widget = forms.NumberInput(attrs={ 'step': 0.50, 'class': 'form-control','placeholder': 'Enter Quantity  (in kg)'}),
		label = 'Quantity'
		)

OrderFormset = formset_factory(OrderNowForm, extra=1)


# class OrderNowForm(forms.ModelForm):
# 	class Meta:
# 		model 	= OrderItems
# 		fields 	= ('product', 'weight', )
# 		labels 	= 	{
#             			'product': 'Choose the Product', 
#             			'weight' : 'Quantity (in kg)' 
#         		  	}

# 		widgets =  {
#             			#'product': forms.ModelChoiceField(attrs={ 'class': 'form-control','placeholder': 'Select Product'}), 
#             			'weight' : forms.NumberInput(attrs={ 'step': 0.50, 'class': 'form-control','placeholder': 'Enter Quantity'})
#          			}


# OrderModelFormset = modelformset_factory(
#     OrderItems,
#     fields=('product', 'weight', ),
#     extra=1,
# 	widgets = 	{
#         			'weight'  : forms.NumberInput(attrs={ 'step': 0.50, 'class': 'form-control','placeholder': 'Enter Quantity'})
#          		}
# )

class SupplierForm(forms.ModelForm):
	def __init__(self,data=None,files=None,request=None,recipient_list=None,*args,**kwargs):
		super().__init__(data=data,files=files,request=request,*args,**kwargs)
		self.fields['name'].widget.attrs['placeholder']='name'
		self.fields['address'].widget.attrs['placeholder']='address'
		self.fields['phone'].widget.attrs['placeholder']='phone'
	class Meta:
		model=Supplier
		fields=('name','address','phone')
	
       		

class MaterialsForm(forms.ModelForm):
	class Meta:
		model  = raw_materials
		fields = '__all__'

class MaterialsOrderForm(forms.ModelForm):
	class Meta:
		model  = materials_order
		fields = '__all__' 

class CreateUserForm(UserCreationForm):
	class Meta:
		model=User
		fields=['username','email','password1','password2']
