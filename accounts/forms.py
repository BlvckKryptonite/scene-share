from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    """
    Custom user registration form extending Django's built-in UserCreationForm.
    Adds an email field and specifies the fields to be used from the User
    model.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating the user's profile information.
    Includes a custom username field and a styled bio textarea.
    """
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'profile-input',
                'placeholder': 'Update your username...'
            }
        )
    )

    class Meta:
        model = Profile
        fields = ['bio']
        widgets = {
            'bio': forms.Textarea(
                attrs={
                    'class': 'profile-input profile-bio',
                    'placeholder': 'Update your bio...',
                    'rows': 2,
                }
            )
        }
