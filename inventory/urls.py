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
 	path('<int:emp_id>/view_works/', views.view_works, name='view_works'),
 	path('<int:emp_id>/add_work/', views.add_work, name='add_work'),

 	# For Customer
 	path('customer/',views.customer,name='customer'),
 	path('add_customer/',views.add_customer,name='add_customer'),
 	path('<int:cus_id>/cust_edit/', views.cust_edit, name='cust_edit'),
 	path('<int:cus_id>/delete_customer/', views.delete_customer, name='delete_customer'),

 	# For orders
 	path('<int:cus_id>/new_order/', views.new_order, name='new_order'),
 		
 	# For product 
 	path('product_details/',views.product_details,name='product_details'),
 	path('add_product/',views.add_product,name='add_product'),
 	path('<int:pro_id>/edit_product/', views.edit_product, name='edit_product'),
 	path('<int:pro_id>/delete_product/', views.delete_product, name='delete_product'),


 	# For Supplier
 	path('supplier/',views.supplier,name='supplier'),
 	path('add_supplier/',views.add_supplier,name='add_supplier'),
 	path('<int:sup_id>/sup_edit/', views.sup_edit, name='sup_edit'),
    path('<int:sup_id>/delete_supplier/',views.delete_supplier,name='delete_supplier'),

    # For Login 
    path('register/',views.registerPage,name='register'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
]