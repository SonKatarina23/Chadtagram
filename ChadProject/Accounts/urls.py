from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'Accounts'

urlpatterns = [
    # Ajax with Vanilla JS
    path('ajax/toggle-follow', views.ToggleFollow.as_view(), name='Toggle_Follow'),

    # Auth stuff
    path('register/', views.Register.as_view(), name='Register'),
    path('login/', auth_views.LoginView.as_view(template_name='Accounts/Login.html'), name='Login'),
    path('logout/',auth_views.LogoutView.as_view(), name='Logout'), 

    # Profile
    path('<username>/', views.Profile.as_view(), name='Profile'),
]
