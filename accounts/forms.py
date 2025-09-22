from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Creating a custom registration form by extending Django's built-in
# UserCreationForm
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True) 

    class Meta:
        model = User  # This form will save data to Django's default User model
        fields = ['username', 'email', 'password1', 'password2']
        # password1 and password2 are used to confirm the password