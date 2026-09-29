from django import forms

from .models import Category, SubCategory


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category

        fields = (
            "name",
            "description",
            "image",
            "display_order",
            "is_active",
        )

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Enter category name",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "placeholder": "Enter category description",
                    "rows": 4,
                }
            ),

            "display_order": forms.NumberInput(
                attrs={
                    "min": 0,
                }
            ),
        }


class SubCategoryForm(forms.ModelForm):

    class Meta:
        model = SubCategory

        fields = (
            "category",
            "name",
            "description",
            "image",
            "display_order",
            "is_active",
        )

        widgets = {
            "category": forms.Select(),

            "name": forms.TextInput(
                attrs={
                    "placeholder": "Enter sub-category name",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "placeholder": "Enter sub-category description",
                    "rows": 4,
                }
            ),

            "display_order": forms.NumberInput(
                attrs={
                    "min": 0,
                }
            ),
        }