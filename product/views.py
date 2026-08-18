from django.shortcuts import render, redirect
import os
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

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