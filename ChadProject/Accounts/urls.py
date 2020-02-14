from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'Accounts'

urlpatterns = [
    path('register/', views.Register.as_view(), name='Register'),
    path('login/', auth_views.LoginView.as_view(template_name='Accounts/Login.html'), name='Login'),
    path('<username>/', views.Profile.as_view(), name='Profile'),
]
