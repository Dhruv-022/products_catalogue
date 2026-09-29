from accounts.models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):

    class Meta:

        model = User

        fields = (
            "username",
            "email",
            "first_name",
            "middle_name",
            "last_name",
            "role",
            "is_active",
        )

    def __init__(self, *args, **kwargs):

        requesting_user = kwargs.pop("requesting_user", None)

        super().__init__(*args, **kwargs)

        self.requesting_user = requesting_user

        if requesting_user and requesting_user.is_owner:

            self.fields["role"].choices = [
                (User.Role.OWNER, "Owner")
            ]

            self.fields["role"].initial = User.Role.OWNER
            self.fields["role"].disabled = True

    def save(self, commit=True):

        user = super().save(commit=False)

        # Server-side enforcement.
        if self.requesting_user and self.requesting_user.is_owner:
            user.role = User.Role.OWNER

        if commit:
            user.save()

        return user


class CustomUserEditForm(forms.ModelForm):

    class Meta:

        model = User

        fields = (
            "username",
            "email",
            "first_name",
            "middle_name",
            "last_name",
            "role",
            "is_active",
        )

    def __init__(self, *args, **kwargs):

        requesting_user = kwargs.pop("requesting_user", None)

        super().__init__(*args, **kwargs)

        self.requesting_user = requesting_user

        if requesting_user and requesting_user.is_owner:

            self.fields["role"].choices = [
                (User.Role.OWNER, "Owner")
            ]

            self.fields["role"].initial = User.Role.OWNER
            self.fields["role"].disabled = True

    def save(self, commit=True):

        user = super().save(commit=False)

        # Owner can never change a user's role.
        if self.requesting_user and self.requesting_user.is_owner:
            user.role = User.Role.OWNER

        if commit:
            user.save()

        return user