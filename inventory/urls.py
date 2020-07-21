from django.urls import path

from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # For Employee 
    path('employee/',views.employee,name='employee'),
    path('add_employee/',views.add_employee,name='add_employee'),
    path('<int:emp_id>/emp_edit/', views.emp_edit, name='emp_edit'),
 	path('<int:emp_id>/delete_employee/', views.delete_employee, name='delete_employee'),
 	path('<int:emp_id>/update_work/', views.update_work, name='update_work'),

 	# For Customer
 	path('customer/',views.customer,name='customer'),
 	path('add_customer/',views.add_customer,name='add_customer'),
 	path('<int:cus_id>/cust_edit/', views.cust_edit, name='cust_edit'),
 	path('<int:cus_id>/delete_customer/', views.delete_customer, name='delete_customer'),

 	# For orders
 	path('<int:cus_id>/new_order/', views.new_order, name='new_order'),
 		
 	# For product 
 	path('add_product/',views.add_product,name='add_product'),
   
]