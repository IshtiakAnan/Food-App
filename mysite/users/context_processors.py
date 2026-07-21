from .models import Profile


def user_role(request):
    if not request.user.is_authenticated:
        return {
            'user_profile': None,
            'profile_role': None,
            'is_manager': False,
            'is_shop_owner': False,
            'is_customer': False,
        }

    profile, _ = Profile.objects.get_or_create(user=request.user)

    return {
        'user_profile': profile,
        'profile_role': profile.role,
        'is_manager': profile.role == Profile.Role.MANAGER,
        'is_shop_owner': profile.role == Profile.Role.SHOP_OWNER,
        'is_customer': profile.role == Profile.Role.CUSTOMER,
    }