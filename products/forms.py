from django import forms
from .models import Brand, Category, SubCategory


class BrandForm(forms.ModelForm):

    class Meta:
        model = Brand

        fields = (
            "name",
            "description",
            "logo",
            "display_order",
            "is_active",
        )

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Enter brand name (e.g. Schneider, ABB)",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Enter brand description or overview",
                    "rows": 4,
                }
            ),
            "display_order": forms.NumberInput(
                attrs={
                    "min": 0,
                }
            ),
        }


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

    brands = forms.ModelMultipleChoiceField(
        queryset=Brand.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        help_text="Select available brands for this sub-category. Leave unselected for 'No Brand'."
    )

    class Meta:
        model = SubCategory

        fields = (
            "category",
            "name",
            "description",
            "image",
            "brands",
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