import json

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View,DetailView
from django.contrib import messages
from django.http import JsonResponse

from . models import User
from Post.models import Post

class Profile(LoginRequiredMixin,DetailView) :
  model = User
  template_name = 'Accounts/Profile.html'
  context_object_name = 'user'
  pk_url_kwarg = 'username'

  def get_object(self) :
    return get_object_or_404(User, username=self.kwargs['username'])

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)

      context["owned_posts"] = Post.objects.filter(owner_id = self.object.id).order_by('-created_at')
      context["is_own_profile"] = self.request.user == self.object
      context["is_following"] = self.request.user in self.object.followers.all()
      return context


class Register(View) :
  def get(self, request, *args, **kwargs) :
    return render(request, 'Accounts/Register.html')
  
  def post(self, request, *args, **kwargs) :
    username = request.POST['username']
    email = request.POST['email']
    password1 = request.POST['password1']
    password2 = request.POST['password2']

    # No Automatic Forms = No Automated Validations either
    # Manual Validations below
    if username == "" or email == "" or password1 == "" or password2 == "" :
      messages.error(request, 'You need to fill in all fields')
      return redirect('Accounts:Register')
    else :
      if password1 != password2 :
        messages.error(request, 'Passwords did not match')
        return redirect('Accounts:Register')
      else :
        if not (any(i.isdigit() for i in password1) and any(i.isalpha() for i in password1)) :
            messages.error(request, 'Password has to contain both letters and numbers')
            return redirect('Accounts:Register')
        else :
          if User.objects.filter(username__iexact=username).exists() :
            messages.error(request, 'Username already exists')
            return redirect('Accounts:Register')
          elif User.objects.filter(email__iexact=email).exists() :
            messages.error(request, 'Email already exists')
            return redirect('Accounts:Register')
          else :
            new_user = User.objects.create(
              username=username,
              email = email
            )
            new_user.set_password(password1)
            new_user.save()
            messages.success(request, "You have successfully created an account")
            return redirect('Accounts:Login')
      

def toggle_follow(request) :
  if request.method == 'POST' :
    username = json.loads(request.body)['username'] # This is a string passed in with axios
    print(f'Username received : {username}')
    profile_seen = User.objects.get(username=username)

    if request.user in profile_seen.followers.all() : # Auth user is following this
      profile_seen.followers.remove(request.user)
      updated_is_following = False
    else :
      #profile_seen.followers.all().append(request.user)
      print(profile_seen.followers.add(request.user))
      updated_is_following = True

    return JsonResponse({
      'updated_is_following' : updated_is_following
    })


