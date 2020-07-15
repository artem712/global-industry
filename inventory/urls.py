from django.urls import path

from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dash/',views.dash,name='dash'),
]