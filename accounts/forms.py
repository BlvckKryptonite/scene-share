from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# Creating a custom registration form by extending Django's built-in
# UserCreationForm
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True) 

    class Meta:
        model = User  # This form will save data to Django's default User model
        fields = ['username', 'email', 'password1', 'password2']
        # password1 and password2 are used to confirm the password


# Profile form
class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'review-input',
            'placeholder': 'Update your username...',
            'style': 'width:100%; padding:0.75rem 1rem; border-radius:6px; border:1px solid #444; background:#2a2a2a; color:#fff; font-size:1rem;'
        })
    )

    class Meta:
        model = Profile
        fields = ['bio']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'review-input',
                'placeholder': 'Update your bio...',
                'rows': 2,
                'style': 'width:100%; padding:0.75rem 1rem; border-radius:6px; border:1px solid #444; background:#2a2a2a; color:#fff; font-size:1rem; resize:none;'
            })
        }


