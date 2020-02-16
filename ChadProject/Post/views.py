import json

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse
from . models import Post, Comment

class PostList(LoginRequiredMixin,ListView) :
  model = Post
  template_name = 'Post/PostList.html'
  context_object_name = 'post_list'

  def get_queryset(self):
      return Post.objects.all().order_by('-created_at')
  
  
class PostDetail(LoginRequiredMixin,DetailView) :
  model = Post
  template_name = 'Post/PostDetail.html'
  context_object_name = 'post'



class ToggleLike(View) :
  def post(self, request, *args, **kwargs) :
    postID = json.loads(request.body)['postID']
    print(f'Post id received : {postID}')
    post = Post.objects.get(id=postID)

    if request.user in post.liked_by.all() :
      updated_like_count = len(post.liked_by.all()) - 1
      post.liked_by.remove(request.user)
      updated_is_liking = False
      
    else :
      updated_like_count = len(post.liked_by.all()) + 1
      post.liked_by.add(request.user)
      updated_is_liking = True
        
    print(f'Updated like count : {updated_like_count}')
    
    return JsonResponse({
      'updated_is_liking' : updated_is_liking,
      'updated_like_count' : updated_like_count
    })


