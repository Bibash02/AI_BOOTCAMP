from django.shortcuts import render, redirect
import os
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
import requests

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
    ai_response = None
    user_prompt = ''

    if request.method == "POST":
        user_prompt = request.POST.get('user_prompt', '').strip()

        if user_prompt:
            api_key = os.getenv('GEMINI_API_KEY')
            endpoint = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"

            headers = {
                'Authorization': f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                'model': "gemini-3.5-flash",
                'messages': [
                    {
                        "role": "system",
                        "content": "You are helpful assestent."
                    },
                    {
                        "role": 'user',
                        "content": user_prompt
                    }
                ],
            }

            try:
                response = request.post(endpoint, headers = headers, json = payload, timeout = 15)

                if response.status_code == 200:
                    data = response.json()
                    ai_response = data['choices'][0]['messages']['content']
                else:
                    ai_response = f"Error: {response.status_code} - {response.text}"

            except Exception as e:
                ai_response = f"Error occur: {str(e)}"
    context = {
        'ai_response': ai_response,
        'user_prompt': user_prompt
    }

    return render(request, 'product/user_dashboard.html', context)

def logout_view(request):
    logout(request)
    return redirect(login)


