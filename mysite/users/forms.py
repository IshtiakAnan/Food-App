from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField()
    role = forms.ChoiceField(choices=Profile.Role.choices, initial=Profile.Role.CUSTOMER)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        user = super().save(commit=commit)

        if commit:
            profile = user.profile
            profile.role = self.cleaned_data.get('role', Profile.Role.CUSTOMER)
            profile.save()

        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_picture", "location"]

