from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),

    # For Login 
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logoutUser/',views.logoutUser,name='logoutUser'),

]