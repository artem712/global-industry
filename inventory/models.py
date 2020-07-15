import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

class Product(models.Model):
	name = models.CharField("Product Name", max_length=30)
	cost = models.IntegerField("Cost per Kg", default=0)
	wages = models.IntegerField("wages per Kg", default=0)
	weight = models.DecimalField(max_digits=7, decimal_places=3) # weight of the products in kg

	def is_available(self, w): # use for reduce_product 
		return ((self.weight - w) >= 0)

	def reduce_product(self, w): # use for customer delivery  
		if(self.is_available(w)):
			self.weight -= w
		else:
			print("There is less or no Product {}".format(self.name)) 
			return

	def add_product(self, w): # Employee add products 
		self.weight += w
		self.save()

	def __str__(self):
		return self.name 

class Salary(models.Model):
	amount = models.DecimalField(max_digits=7, decimal_places=2)
	paid_status = models.BooleanField(default=False)
	date = models.DateTimeField('date of salary updated')

	def add_amount(self, amt):
		self.amount += amt 
		self.save() 

class Employee(models.Model):
	name = models.CharField("Employee Name", max_length=30)
	designation = models.CharField("Designation", max_length=30)
	address = models.CharField(max_length=70)
	phone = models.CharField("Phone Number", max_length=11)
	dob = models.DateTimeField('date of birth')
	doj = models.DateTimeField('date of Joined')
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	gender = models.BooleanField(default=False) # true == boy & false == girl
	salary = models.ForeignKey(Salary, on_delete=models.CASCADE)

	def __str__(self):
		return self.name ; 

	def update_work(self, weight):
		self.product.add_product(weight)
		self.salary.add_amount(weight * product.wage)
		self.save()

class Customer(models.Model):
	name = models.CharField("Customer Name", max_length=30)
	address = models.CharField(max_length=70)
	phone = models.CharField("Phone Number", max_length=11)

	def __str__(self):
		return self.name

class Raw_Material(models.Model):
	name = models.CharField("Raw Material Name", max_length=30)
	cost = models.DecimalField(max_digits=6, decimal_places=2) # Cost per Kg

	def __str__(self):
		return self.name ;

class Stock(models.Model):  #contains the available stocks in company
	products = models.ForeignKey(Product, on_delete=models.CASCADE) # Available List of Products and their weight
	raw_materials = models.ForeignKey(Raw_Material, on_delete=models.CASCADE) # Available List of Products and their weight
	Amount = models.DecimalField(max_digits=11, decimal_places=2) # company's accounts   


class Order(models.Model):
	products = models.ForeignKey(Product, on_delete=models.CASCADE) # List of Products
	Odate = models.DateTimeField('date of ordered')
	Ddate = models.DateTimeField('date of delivery')
	d_status = models.BooleanField(default=False) # delivery status
  


class Supplier(models.Model):
	name = models.CharField("Supplier Name", max_length=30)
	address = models.CharField(max_length=70)
	phone = models.CharField("Phone Number", max_length=11)
	
	def __str__(self):
		return self.name 