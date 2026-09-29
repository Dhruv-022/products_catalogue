from django.urls import path

from . import views


app_name = "products"


urlpatterns = [

    # -------------------------
    # Categories
    # -------------------------

    path(
        "categories/",
        views.category_list,
        name="category_list",
    ),

    path(
        "categories/create/",
        views.category_create,
        name="category_create",
    ),

    path(
        "categories/<int:category_id>/edit/",
        views.category_edit,
        name="category_edit",
    ),

    path(
        "categories/<int:category_id>/toggle-status/",
        views.category_toggle_status,
        name="category_toggle_status",
    ),

    path(
        "categories/<int:category_id>/delete/",
        views.category_delete,
        name="category_delete",
    ),


    # -------------------------
    # Sub-Categories
    # -------------------------

    path(
        "subcategories/",
        views.subcategory_list,
        name="subcategory_list",
    ),

    path(
        "subcategories/create/",
        views.subcategory_create,
        name="subcategory_create",
    ),

    path(
        "subcategories/<int:subcategory_id>/edit/",
        views.subcategory_edit,
        name="subcategory_edit",
    ),

    path(
        "subcategories/<int:subcategory_id>/toggle-status/",
        views.subcategory_toggle_status,
        name="subcategory_toggle_status",
    ),

    path(
        "subcategories/<int:subcategory_id>/delete/",
        views.subcategory_delete,
        name="subcategory_delete",
    ),

]