from django.urls import path

from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('employee/',views.employee,name='employee'),
    path('add_employee/',views.add_employee,name='add_employee'),
]