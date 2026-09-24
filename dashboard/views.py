from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


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

            return redirect("dashboard:home")

        return render(
            request,
            "dashboard/login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(
        request,
        "dashboard/login.html"
    )


@login_required
def dashboard_home(request):

    return render(
        request,
        "dashboard/home.html"
    )


@login_required
def logout_view(request):

    logout(request)

    return redirect("dashboard:login")