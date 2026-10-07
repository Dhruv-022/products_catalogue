from django.db.models import Prefetch
from django.shortcuts import render

from products.models import Category, SubCategory

import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

logger = logging.getLogger(__name__)


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
        .order_by(
            "display_order",
            "name",
        )
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
        .order_by(
            "display_order",
            "name",
        )
    )

    return render(
        request,
        "public/products.html",
        {
            "categories": categories,
        },
    )


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data.get('phone', 'Not provided')
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            email_subject = f"[Website Enquiry] {subject}"
            email_body = (
                f"New customer enquiry received from Al Baraq website:\n\n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n"
                f"Subject: {subject}\n\n"
                f"Message:\n{message}"
            )

            try:
                send_mail(
                    subject=email_subject,
                    message=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.COMPANY_INBOX_EMAIL],
                    fail_silently=False,
                )

                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'success', 'message': 'Thank you! Your enquiry has been sent successfully.'})

                return render(request, 'public/contact.html', {'form': ContactForm(), 'success': True})

            except Exception as e:
                logger.error(f"Error sending email via Brevo: {e}")
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'error', 'message': 'Could not send email. Please try again later.'}, status=500)

        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    # GET request loads the page
    return render(request, 'public/contact.html', {'form': ContactForm()})