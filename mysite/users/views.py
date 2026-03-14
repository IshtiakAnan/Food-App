from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from food.models import Item
from .forms import RegisterForm
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
    user_profile = Profile.objects.filter(user=request.user).first()
    profile_picture_url = None

    if user_profile and user_profile.profile_picture and user_profile.profile_picture.name != 'default.jpg':
        profile_picture_url = user_profile.profile_picture.url

    context = {
        'display_name': full_name or request.user.username,
        'total_items': Item.objects.count(),
        'profile_picture_url': profile_picture_url,
    }

    return render(request, 'users/user_profile.html', context)
