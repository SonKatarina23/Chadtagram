from django import forms
from crispy_forms.helper import FormHelper, Layout
from . models import Post

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ("photo", "captions")
