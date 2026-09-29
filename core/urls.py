from django.contrib import admin
from django.urls import include, path


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "dashboard/",
        include("dashboard.urls")
    ),

    path(
        "accounts/",
        include("accounts.urls")
    ),

    path(
        "products/",
        include("products.urls")
    ),

    path(
        "",
        include("public.urls")
    ),

]