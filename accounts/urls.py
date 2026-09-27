from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("users/", views.user_list, name="user_list"),
    path("users/create/", views.user_create, name="user_create"),
    path("users/<int:user_id>/", views.user_detail, name="user_detail"),
    path("users/<int:user_id>/edit/", views.user_edit, name="user_edit"),
    path(
        "users/<int:user_id>/toggle-status/",
        views.user_toggle_status,
        name="user_toggle_status",
    ),

    path(
        "users/<int:user_id>/delete/", views.user_delete, name="user_delete"
    ),
]