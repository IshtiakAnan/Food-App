from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from food.models import Item
from .forms import ProfileUpdateForm, RegisterForm, UserUpdateForm
from .models import Profile

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}, your account has been created successfully!')
            return redirect('login')
    else:
        form = RegisterForm()

    context = {
        'form': form
    }

    return render(request, 'users/register.html', context)


@login_required(login_url='login')
def profile(request):
    full_name = request.user.get_full_name().strip()
    user_profile, _ = Profile.objects.get_or_create(user=request.user)
    profile_picture_url = None

    if user_profile and user_profile.profile_picture and user_profile.profile_picture.name != 'default.jpg':
        profile_picture_url = user_profile.profile_picture.url

    context = {
        'display_name': full_name or request.user.username,
        'total_items': Item.objects.count(),
        'profile_picture_url': profile_picture_url,
        'profile_location': user_profile.location,
        'profile_role': user_profile.role,
    }

    return render(request, 'users/user_profile.html', context)


@login_required(login_url='login')
def update_profile(request):
    user_profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=user_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile_picture_url': user_profile.profile_picture.url if user_profile.profile_picture and user_profile.profile_picture.name != 'default.jpg' else None,
        'profile_role': user_profile.role,
    }

    return render(request, 'users/edit_profile.html', context)
