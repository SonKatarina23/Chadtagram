from django.urls import path
from . import views

app_name = 'Post'

urlpatterns = [
    path('', views.PostList.as_view(), name='post-list')
]
