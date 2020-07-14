import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

class Product(models.Model):
	name = models.CharField("Product Name", max_length=30)
	cost = models.IntegerField("Cost per Kg", default=0)
	wages = models.IntegerField("wages per Kg", default=0)
	weight = models.DecimalField(max_digits=7, decimal_places=3) # weight of the products in kg

	def __str__(self):
		return self.name ;

class Salary(models.Model):
	amount = models.DecimalField(max_digits=7, decimal_places=2)
	paid_status = models.BooleanField(default=False) 
	date =  models.DateTimeField('Date of ')

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


class Employee(models.Model):
	name = models.CharField("Employee Name", max_length=30)
	designation = models.CharField("Designation", max_length=30)
	address = models.CharField(max_length=70)
	phone = models.CharField("Phone Number", max_length=11)
	salary = models.ForeignKey(Salary, on_delete=models.CASCADE)
	dob = models.DateTimeField('date of birth')
	doj = models.DateTimeField('date of Joined')

	def __str__(self):
		return self.name ; 


class Customer(models.Model):
	name = models.CharField("Customer Name", max_length=30)
	address = models.CharField(max_length=70)
	phone = models.CharField("Phone Number", max_length=11)
	orders = models.ForeignKey(Order, on_delete=models.CASCADE)

	def __str__(self):
		return self.name ; 


class Supplier(models.Model):
	name = models.CharField("Supplier Name", max_length=30)
	address = models.CharField(max_length=70)
	phone = models.CharField("Phone Number", max_length=11)
	
	def __str__(self):
		return self.name ; 