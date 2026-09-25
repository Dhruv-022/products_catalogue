from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render


def login_view(request):
  if request.user.is_authenticated:
    return redirect("dashboard:home")

  if request.method == "POST":
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      username = form.cleaned_data.get("username")
      password = form.cleaned_data.get("password")
      user = authenticate(request, username=username, password=password)
      if user is not None:
        login(request, user)
        # Handles any ?next=/path/ parameter automatically
        next_url = request.GET.get("next") or "dashboard:home"
        return redirect(next_url)
  else:
    form = AuthenticationForm()

  return render(request, "dashboard/login.html", {"form": form})


def logout_view(request):
  logout(request)
  return redirect("dashboard:login")