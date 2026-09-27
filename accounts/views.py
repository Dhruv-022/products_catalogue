from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from accounts.decorators import system_admin_required
from accounts.forms import CustomUserCreationForm, CustomUserEditForm
from accounts.models import User
from django.contrib.auth.decorators import login_required


@system_admin_required
def user_list(request):
  users = User.objects.all().order_by("-date_joined")
  return render(request, "accounts/user_list.html", {"users": users})


@system_admin_required
def user_detail(request, user_id):
  target_user = get_object_or_404(User, id=user_id)
  return render(request, "accounts/user_detail.html", {"target_user": target_user})


@system_admin_required
def user_create(request):
  if request.method == "POST":
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      messages.success(request, f"User {user.username} created successfully.")
      return redirect("accounts:user_list")
  else:
    form = CustomUserCreationForm()
  return render(
      request,
      "accounts/user_form.html",
      {"form": form, "title": "Create User"},
  )


@system_admin_required
def user_edit(request, user_id):
  user_instance = get_object_or_404(User, id=user_id)
  if request.method == "POST":
    form = CustomUserEditForm(request.POST, instance=user_instance)
    if form.is_valid():
      form.save()
      messages.success(
          request, f"User {user_instance.username} updated successfully."
      )
      return redirect("accounts:user_list")
  else:
    form = CustomUserEditForm(instance=user_instance)
  return render(
      request,
      "accounts/user_form.html",
      {"form": form, "title": f"Edit User: {user_instance.username}"},
  )


@system_admin_required
def user_toggle_status(request, user_id):
  user_instance = get_object_or_404(User, id=user_id)
  if user_instance == request.user:
    messages.error(request, "You cannot deactivate your own account.")
    return redirect("accounts:user_list")

  user_instance.is_active = not user_instance.is_active
  user_instance.save()
  status_str = "activated" if user_instance.is_active else "deactivated"
  messages.info(request, f"User {user_instance.username} has been {status_str}.")
  return redirect("accounts:user_list")


@system_admin_required
def user_delete(request, user_id):
  user_instance = get_object_or_404(User, id=user_id)

  # Self-deletion safety check
  if user_instance == request.user:
    messages.error(request, "You cannot delete your own account.")
    return redirect("accounts:user_list")

  if request.method == "POST":
    username = user_instance.username
    user_instance.delete()
    messages.success(request, f"User {username} was deleted permanently.")
    return redirect("accounts:user_list")

  return render(
      request, "accounts/user_confirm_delete.html", {"target_user": user_instance}
  )

from django.contrib.auth import authenticate, login, logout


def login_view(request):
  if request.user.is_authenticated:
    return redirect("dashboard:home")

  if request.method == "POST":
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)

      # Smart role-based redirection post-login
      if user.role == User.Role.OWNER:
        return redirect("dashboard:owner_dashboard")
      elif user.role == User.Role.SYSTEM_ADMIN:
        return redirect("dashboard:home")
      else:
        # Default fallback for Managers/Staff
        return redirect("dashboard:home")

    return render(
        request,
        "dashboard/login.html",
        {"error": "Invalid username or password."},
    )

  return render(request, "dashboard/login.html")


@login_required
def logout_view(request):
  logout(request)
  return redirect("dashboard:login")