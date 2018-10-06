from django.urls import include, path
from account import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('', views.loginview, name='main-view'),
	path('login/', auth_views.LoginView.as_view(), name='login')

]