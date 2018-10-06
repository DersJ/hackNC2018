from django.urls import include, path
from account import views

urlpatterns = [
	path('', views.loginview, name='main-view'),

]