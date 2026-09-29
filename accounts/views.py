from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import (
    can_manage_user,
    owner_or_admin_required,
    system_admin_required,
)

from accounts.forms import (
    CustomUserCreationForm,
    CustomUserEditForm,
)

from accounts.models import User


@owner_or_admin_required
def user_list(request):

    if request.user.is_owner:
        users = User.objects.filter(
            role=User.Role.OWNER
        ).order_by("-date_joined")
    else:
        users = User.objects.all().order_by("-date_joined")

    return render(
        request,
        "accounts/user_list.html",
        {"users": users}
    )


@owner_or_admin_required
def user_detail(request, user_id):

    target_user = get_object_or_404(
        User,
        id=user_id
    )

    if not can_manage_user(request.user, target_user):
        raise PermissionDenied(
            "You do not have permission to manage this user."
        )

    return render(
        request,
        "accounts/user_detail.html",
        {"target_user": target_user}
    )


@owner_or_admin_required
def user_create(request):

    if request.method == "POST":

        form = CustomUserCreationForm(
            request.POST,
            requesting_user=request.user
        )

        if form.is_valid():

            user = form.save(commit=False)

            # Owners can only create Owner accounts.
            if request.user.is_owner:
                user.role = User.Role.OWNER

            user.save()

            messages.success(
                request,
                f"User {user.username} created successfully."
            )

            return redirect("accounts:user_list")

    else:

        form = CustomUserCreationForm(
            requesting_user=request.user
        )

    return render(
        request,
        "accounts/user_form.html",
        {
            "form": form,
            "title": "Create User",
        },
    )


@owner_or_admin_required
def user_edit(request, user_id):

    user_instance = get_object_or_404(
        User,
        id=user_id
    )

    if not can_manage_user(request.user, user_instance):
        raise PermissionDenied(
            "You do not have permission to edit this user."
        )

    if request.method == "POST":

        form = CustomUserEditForm(
            request.POST,
            instance=user_instance,
            requesting_user=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                f"User {user_instance.username} updated successfully."
            )

            return redirect("accounts:user_list")

    else:

        form = CustomUserEditForm(
            instance=user_instance,
            requesting_user=request.user
        )

    return render(
        request,
        "accounts/user_form.html",
        {
            "form": form,
            "title": f"Edit User: {user_instance.username}",
        },
    )


@owner_or_admin_required
def user_toggle_status(request, user_id):

    user_instance = get_object_or_404(
        User,
        id=user_id
    )

    if not can_manage_user(request.user, user_instance):
        raise PermissionDenied(
            "You do not have permission to modify this user."
        )

    if user_instance == request.user:

        messages.error(
            request,
            "You cannot deactivate your own account."
        )

        return redirect("accounts:user_list")

    user_instance.is_active = not user_instance.is_active
    user_instance.save()

    status_str = (
        "activated"
        if user_instance.is_active
        else "deactivated"
    )

    messages.info(
        request,
        f"User {user_instance.username} has been {status_str}."
    )

    return redirect("accounts:user_list")


@owner_or_admin_required
def user_delete(request, user_id):

    user_instance = get_object_or_404(
        User,
        id=user_id
    )

    if not can_manage_user(request.user, user_instance):
        raise PermissionDenied(
            "You do not have permission to delete this user."
        )

    if user_instance == request.user:

        messages.error(
            request,
            "You cannot delete your own account."
        )

        return redirect("accounts:user_list")

    if request.method == "POST":

        username = user_instance.username

        user_instance.delete()

        messages.success(
            request,
            f"User {username} was deleted permanently."
        )

        return redirect("accounts:user_list")

    return render(
        request,
        "accounts/user_confirm_delete.html",
        {
            "target_user": user_instance
        }
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard:home")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            next_url = (
                request.GET.get("next")
                or "dashboard:home"
            )

            return redirect(next_url)

        return render(
            request,
            "dashboard/login.html",
            {
                "error": "Invalid username or password."
            },
        )

    return render(
        request,
        "dashboard/login.html"
    )


@owner_or_admin_required
def logout_view(request):

    logout(request)

    return redirect("dashboard:login")