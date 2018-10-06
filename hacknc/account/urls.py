from django.urls import include, path
from account import views

urlpatterns = [
	path('index/', views.loginview, name='main-view'),

]