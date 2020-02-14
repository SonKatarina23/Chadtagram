from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from . models import User
from Post.models import Post

class Profile(DetailView) :
  model = User
  template_name = 'Accounts/Profile.html'
  context_object_name = 'user'
  pk_url_kwarg = 'username'

  def get_object(self) :
    return get_object_or_404(User, username=self.kwargs['username'])

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      owned_posts = Post.objects.filter(owner_id = self.object.id).order_by('-created_at')
      context["owned_posts"] = owned_posts 
      return context
  