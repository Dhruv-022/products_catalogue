from accounts.views import login_view, logout_view
from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]