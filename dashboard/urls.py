

from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    path(
        "catalogue-test/",
        views.catalogue_management_test,
        name="cat_test"
    ),

    path(
        "admin-test/",
        views.admin_only_test,
        name="admin_test"
    ),
]