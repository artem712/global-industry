from django.contrib import admin

from .models import Employee, Product, Salary 

# Register your models here.

admin.site.register(Salary)
admin.site.register(Employee)
admin.site.register(Product)