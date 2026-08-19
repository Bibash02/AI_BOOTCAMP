from django.urls import path
from .views import register_view, login_view, admin_dashboard, user_dashboard

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),

    path('admin-panel', admin_dashboard, name='admin-dashboard'),
    path('user-panel', user_dashboard, name='user-dashboard'),
]