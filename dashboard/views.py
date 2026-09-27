from accounts.decorators import owner_or_admin_required, system_admin_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render


@login_required
def home(request):
  return render(request, "dashboard/home.html", {"user": request.user})


def login_view(request):
  if request.user.is_authenticated:
    return redirect("dashboard:home")

  if request.method == "POST":
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      next_url = request.GET.get("next") or "dashboard:home"
      return redirect(next_url)

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


@owner_or_admin_required
def catalogue_management_test(request):
  """Only System Admin and Owner can access this view."""
  return HttpResponse(
      f"Hello {request.user.first_name}, you have access to Catalogue"
      f" Management as a {request.user.get_role_display()}."
  )


@system_admin_required
def admin_only_test(request):
  """Only System Admin can access this view."""
  return HttpResponse(
      f"System Administration Portal. Access granted to"
      f" {request.user.username}."
  )


from accounts.decorators import owner_required


@owner_required
def owner_dashboard(request):
  """Dedicated dashboard view exclusively for the Owner role."""
  return render(request, "dashboard/owner_home.html", {"user": request.user})