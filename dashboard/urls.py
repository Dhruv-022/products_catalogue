from accounts.views import login_view, logout_view
from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    path("catalogue-test/", views.catalogue_management_test, name="cat_test"),
    path("admin-test/", views.admin_only_test, name="admin_test"),
    path("owner/", views.owner_dashboard, name="owner_dashboard"),
]