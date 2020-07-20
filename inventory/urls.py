from django.urls import path

from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('employee/',views.employee,name='employee'),
    path('add_employee/',views.add_employee,name='add_employee'),
    path('<int:emp_id>/emp_edit/', views.emp_edit, name='emp_edit'),
 	path('<int:emp_id>/delete_employee/', views.delete_employee, name='delete_employee'),
 	path('customer/',views.customer,name='customer'),
 	path('add_customer/',views.add_customer,name='add_customer'),
 	path('<int:cus_id>/cust_edit/', views.cust_edit, name='cust_edit'),
 	path('<int:cus_id>/delete_customer/', views.delete_customer, name='delete_customer'),
       
]