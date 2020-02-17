from django import forms
from . models import User

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = (
          'first_name', 'last_name', 'username', 'email', 'gender', 'phone_number', 'bio', 'profile_picture',
        )
