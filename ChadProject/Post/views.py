from django.shortcuts import render
from django.http import HttpResponse

def home(request) :
  return render(request, 'Post/PostList.html')
