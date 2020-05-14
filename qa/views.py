from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'base.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return HttpResponse('Authentication Successfully')
            else:
                return HttpResponse('Invalid Login')
        
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

@login_required
def logged_in(request):
    return render(request, 'base.html', {'section': 'logged-in'})