from django.shortcuts import render
from django.http import HttpResponse

def home(request) :
  return HttpResponse('This is Post-List View or also known as Home Page')
