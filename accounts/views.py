from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm

# Create your views here.


def register(request):
    """
    Handle user registration.

    Renders the registration form on GET requests.
    On POST, validates and creates a new user, then redirects to login.
    Displays a success message upon successful registration.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # This creates a new user in the database
            username = form.cleaned_data.get('username')
            messages.success(
                request,
                f'Account created for {username}! You can now log in.'
            )
            # Redirect to login page after registration
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    """
    Display and handle updates to the user's profile.

    Allows users to update their profile and username.
    On POST, saves changes and redirects to the profile page.
    """
    user = request.user

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user.profile)
        if form.is_valid():
            # Save bio
            profile = form.save(commit=False)
            profile.save()
            # Save username
            user.username = form.cleaned_data['username']
            user.save()
            messages.success(
                request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(
            instance=user.profile,
            initial={'username': user.username}
        )

    return render(request, 'accounts/profile.html', {'form': form})
