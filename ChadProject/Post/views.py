import json

from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Q

from Accounts.views import Suggest
from . models import Post, Comment
from . forms import PostForm


##############################################  POST  ###################################################


class CreatePost(CreateView) :
  model = Post
  form_class = PostForm
  template_name = 'Post/PostForm.html'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["form"] = self.get_form_class()
      context["title"] = 'Create New Post'
      return context
  
  def form_valid(self, form) :
    form.instance.owner = self.request.user
    return super().form_valid(form)


class PostList(LoginRequiredMixin,ListView) :
  model = Post
  template_name = 'Post/PostList.html'
  context_object_name = 'post_list'

  def get_queryset(self):
      # Only shows post from users whom current user follows
      qs = Post.objects.filter(
        Q(owner__followers=self.request.user) | 
        Q(owner=self.request.user)
      ).order_by('-created_at').distinct()
      return qs
  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["suggestions"] = Suggest(self.request.user)
      return context
  
  
   
class PostDetail(LoginRequiredMixin,DetailView) :
  model = Post
  template_name = 'Post/PostDetail.html'
  context_object_name = 'post'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["comments"] = self.object.get_all_comments()
      context["is_own"] = self.object.owner == self.request.user
      context["is_following"] = self.request.user in self.object.owner.followers.all()
      return context
  

class UpdatePost(UpdateView) :
  model = Post
  form_class = PostForm
  template_name = 'Post/PostForm.html'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["title"] = 'Update Post' 
      return context
  

class DeletePost(DeleteView) :
  model = Post
  success_url = reverse_lazy('Post:List')


##############################################  COMMENT  ###################################################

class AddComment(LoginRequiredMixin, View) :
  def post(self, request, *args, **kwargs) :
    postID = request.POST['postID']
    comment = request.POST['comment']

    post = Post.objects.get(id=postID)
    Comment.objects.create(owner = request.user, post = post, comment=comment)
    return redirect('Post:Detail', pk = post.id)
  

class DeleteComment(LoginRequiredMixin, DeleteView) :
  model = Comment
  
  def get_success_url(self) :
    post = self.object.post
    return reverse_lazy('Post:Detail', kwargs= {'pk' : post.id})
  

##############################################  AJAX  ###################################################

class ToggleLike(LoginRequiredMixin, View) :
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

class LikePost(LoginRequiredMixin, View) : 
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