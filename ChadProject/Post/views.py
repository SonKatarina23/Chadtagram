from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Post, Comment

class PostList(ListView) :
  model = Post
  template_name = 'Post/PostList.html'
  context_object_name = 'post_list'

  
  