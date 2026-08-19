from django.shortcuts import render, redirect
import os
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('register')
    else:
        form = UserCreationForm

    return render(request, 'product/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()

            # check if the user is superuser or not
            if user.is_staff or user.is_superuser:
                return redirect('admin-panel')
            else:
                return redirect('user-dashboard')
    else:
        form = AuthenticationForm()
    return render(request, "product/login.html", {'form': form})

@user_passes_test(lambda u:u.is_staff, login_url='login')
def admin_dashboard(request):
    return render(request, 'product/admin_dashboard.html')

@login_required(login_url='login')
def user_dashboard(request):
    return render(request, 'product/user_dashboard.html')

def logout_view(request):
    logout(request)
    return redirect(login)