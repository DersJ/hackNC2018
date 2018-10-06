from django.http import HttpResponse
from django.shortcuts import render, redirect
from account.forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.views import generic

def loginview(request):
	return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

class ProfileView(generic.DetailView):

    context_object_name = 'tournament'
    template_name = 'registration/profile.html'

    def get_object(self):
        return self.request.user