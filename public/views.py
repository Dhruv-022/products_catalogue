from django.shortcuts import render


def home_view(request):
  """Public Home Page"""
  return render(request, "public/home.html")


def products_view(request):
  """Public Products Catalogue Page"""
  return render(request, "public/products.html")


def about_view(request):
  """About Us Page"""
  return render(request, "public/about.html")


def contact_view(request):
  """Contact Us Page"""
  return render(request, "public/contact.html")