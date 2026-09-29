from django.db.models import Prefetch
from django.shortcuts import render

from products.models import Category, SubCategory


def home(request):

    return render(
        request,
        "public/home.html"
    )


def about(request):

    return render(
        request,
        "public/about.html"
    )


def products(request):

    active_subcategories = (
        SubCategory.objects
        .filter(is_active=True)
        .order_by("display_order", "name")
    )

    categories = (
        Category.objects
        .filter(is_active=True)
        .prefetch_related(
            Prefetch(
                "subcategories",
                queryset=active_subcategories,
            )
        )
        .order_by("display_order", "name")
    )

    return render(
        request,
        "public/products.html",
        {
            "categories": categories,
        },
    )


def contact(request):

    return render(
        request,
        "public/contact.html"
    )

