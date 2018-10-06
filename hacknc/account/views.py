from django.http import HttpResponse
from django.shortcuts import render

def loginview(request):
	return render(request, 'landing.html')