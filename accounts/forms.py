from accounts.models import User
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class CustomUserCreationForm(UserCreationForm):

  class Meta:
    model = User
    fields = (
        'username',
        'email',
        'first_name',
        'middle_name',
        'last_name',
        'role',
        'is_active',
    )


class CustomUserEditForm(forms.ModelForm):

  class Meta:
    model = User
    fields = (
        'username',
        'email',
        'first_name',
        'middle_name',
        'last_name',
        'role',
        'is_active',
    )