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

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)

      # Retriving comments
      comments = Comment.objects.filter(post=self.object).order_by('-created_at')
      context["comments"] = comments

      # Check if this post is his/her own post
      is_own = self.object.owner == self.request.user
      context["is_own"] = is_own

      # Check if this post'sowner is followed by current user
      is_following = self.request.user in self.object.owner.followers.all()
      context["is_following"] = is_following

      return context
  


class ToggleLike(View) :
  def post(self, request, *args, **kwargs) :
    postID = json.loads(request.body)['postID']
    post = Post.objects.get(id=postID)

    if request.user in post.liked_by.all() :
      updated_like_count = len(post.liked_by.all()) - 1
      post.liked_by.remove(request.user)
      updated_is_liking = False
      
    else :
      updated_like_count = len(post.liked_by.all()) + 1
      post.liked_by.add(request.user)
      updated_is_liking = True
    
    return JsonResponse({
      'updated_is_liking' : updated_is_liking,
      'updated_like_count' : updated_like_count
    })

class LikePost(View) : 
  def post(self, request, *args, **kwargs) :
    postID = json.loads(request.body)['postID']
    post = Post.objects.get(id=postID)

    if request.user in post.liked_by.all() :
      updated_like_count = len(post.liked_by.all())
    else :
      updated_like_count = len(post.liked_by.all()) + 1
      post.liked_by.add(request.user)

    return JsonResponse({
      'updated_like_count' : updated_like_count
    })