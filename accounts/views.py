from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm

# Create your views here.

# I am defining the registration page view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # This creates a new user in the database
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


# Profile page view 
@login_required
def profile(request):
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
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user.profile, initial={'username': user.username})

    return render(request, 'accounts/profile.html', {'form': form})

