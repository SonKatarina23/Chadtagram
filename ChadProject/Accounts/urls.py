from django.urls import path
from . import views

app_name = 'Accounts'

urlpatterns = [
    path('<username>/', views.Profile.as_view(), name='Profile')
]
