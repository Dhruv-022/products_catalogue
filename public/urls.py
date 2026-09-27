from django.urls import path
from . import views

app_name = "public"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("catalogue/", views.products_view, name="products"),
    path("about/", views.about_view, name="about"),
    path("contact/", views.contact_view, name="contact"),
]