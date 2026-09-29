from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import owner_or_admin_required
from django.core.exceptions import PermissionDenied
from .forms import CategoryForm, SubCategoryForm
from .models import Category, SubCategory


# ============================================================
# CATEGORY MANAGEMENT
# ============================================================

@owner_or_admin_required
def category_list(request):

    categories = Category.objects.all().order_by(
        "display_order",
        "name",
    )

    return render(
        request,
        "products/category_list.html",
        {
            "categories": categories,
        },
    )


@owner_or_admin_required
def category_create(request):

    if request.method == "POST":

        form = CategoryForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            category = form.save()

            messages.success(
                request,
                f"Category '{category.name}' created successfully.",
            )

            return redirect(
                "products:category_list"
            )

    else:

        form = CategoryForm()

    return render(
        request,
        "products/category_form.html",
        {
            "form": form,
            "title": "Create Category",
        },
    )


@owner_or_admin_required
def category_edit(request, category_id):

    category = get_object_or_404(
        Category,
        id=category_id,
    )

    if request.method == "POST":

        form = CategoryForm(
            request.POST,
            request.FILES,
            instance=category,
        )

        if form.is_valid():

            category = form.save()

            messages.success(
                request,
                f"Category '{category.name}' updated successfully.",
            )

            return redirect(
                "products:category_list"
            )

    else:

        form = CategoryForm(
            instance=category,
        )

    return render(
        request,
        "products/category_form.html",
        {
            "form": form,
            "title": f"Edit Category: {category.name}",
            "category": category,
        },
    )


@owner_or_admin_required
def category_toggle_status(request, category_id):

    # Status changes should only happen through POST.
    if request.method != "POST":
        return redirect(
            "products:category_list"
        )

    category = get_object_or_404(
        Category,
        id=category_id,
    )

    category.is_active = not category.is_active

    category.save()

    status = (
        "activated"
        if category.is_active
        else "hidden"
    )

    messages.info(
        request,
        f"Category '{category.name}' has been {status}.",
    )

    return redirect(
        "products:category_list"
    )


@owner_or_admin_required
def category_delete(request, category_id):

    category = get_object_or_404(
        Category,
        id=category_id,
    )

    if request.method == "POST":

        category_name = category.name

        category.delete()

        messages.success(
            request,
            f"Category '{category_name}' was deleted permanently.",
        )

        return redirect(
            "products:category_list"
        )

    return render(
        request,
        "products/category_confirm_delete.html",
        {
            "category": category,
        },
    )


# ============================================================
# SUB-CATEGORY MANAGEMENT
# ============================================================

@owner_or_admin_required
def subcategory_list(request):

    subcategories = SubCategory.objects.select_related(
        "category"
    ).order_by(
        "category__display_order",
        "category__name",
        "display_order",
        "name",
    )

    return render(
        request,
        "products/subcategory_list.html",
        {
            "subcategories": subcategories,
        },
    )


@owner_or_admin_required
def subcategory_create(request):

    if request.method == "POST":

        form = SubCategoryForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            subcategory = form.save()

            messages.success(
                request,
                f"Sub-category '{subcategory.name}' created successfully.",
            )

            return redirect(
                "products:subcategory_list"
            )

    else:

        form = SubCategoryForm()

    return render(
        request,
        "products/subcategory_form.html",
        {
            "form": form,
            "title": "Create Sub-Category",
        },
    )


@owner_or_admin_required
def subcategory_edit(request, subcategory_id):

    subcategory = get_object_or_404(
        SubCategory,
        id=subcategory_id,
    )

    if request.method == "POST":

        form = SubCategoryForm(
            request.POST,
            request.FILES,
            instance=subcategory,
        )

        if form.is_valid():

            subcategory = form.save()

            messages.success(
                request,
                f"Sub-category '{subcategory.name}' updated successfully.",
            )

            return redirect(
                "products:subcategory_list"
            )

    else:

        form = SubCategoryForm(
            instance=subcategory,
        )

    return render(
        request,
        "products/subcategory_form.html",
        {
            "form": form,
            "title": f"Edit Sub-Category: {subcategory.name}",
            "subcategory": subcategory,
        },
    )


@owner_or_admin_required
def subcategory_toggle_status(request, subcategory_id):

    if request.method != "POST":
        raise PermissionDenied(
            "Invalid request method."
        )

    subcategory = get_object_or_404(
        SubCategory,
        id=subcategory_id,
    )

    subcategory.is_active = not subcategory.is_active
    subcategory.save()

    status = (
        "activated"
        if subcategory.is_active
        else "hidden"
    )

    messages.info(
        request,
        f"Sub-category '{subcategory.name}' has been {status}.",
    )

    return redirect(
        "products:subcategory_list"
    )

@owner_or_admin_required
def subcategory_delete(request, subcategory_id):

    subcategory = get_object_or_404(
        SubCategory,
        id=subcategory_id,
    )

    if request.method == "POST":

        subcategory_name = subcategory.name

        subcategory.delete()

        messages.success(
            request,
            f"Sub-category '{subcategory_name}' was deleted permanently.",
        )

        return redirect(
            "products:subcategory_list"
        )

    return render(
        request,
        "products/subcategory_confirm_delete.html",
        {
            "subcategory": subcategory,
        },
    )