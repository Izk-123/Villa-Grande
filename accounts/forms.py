from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Role

class CustomUserCreationForm(UserCreationForm):
    role = forms.ModelChoiceField(queryset=Role.objects.all(), required=False)

    class Meta:
        model = User
        fields = ('username', 'role', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Assign role to profile
            role = self.cleaned_data.get('role')
            if role:
                user.profile.role = role
                user.profile.save()
        return user

class UserUpdateForm(UserChangeForm):
    password = None      # remove password field from update form
    role = forms.ModelChoiceField(queryset=Role.objects.all(), required=False)

    class Meta:
        model = User
        fields = ('username', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            role = self.cleaned_data.get('role')
            if role:
                user.profile.role = role
                user.profile.save()
        return user