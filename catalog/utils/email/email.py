from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from products.models import Order


def send_email_confirm(request, user, new_email):
    confirm_url = request.build_absolute_uri(reverse("accounts:confirm_email"))
    confirm_url += f"?user={user.id}&email={new_email}"
    subject = "Confirm new email"
    message = f"Hello, {user.username}! You want to change your email. To confirm click here: {confirm_url}"
    send_mail(subject, message, "noreply@gmail.com", [new_email], fail_silently=False)
    messages.info(request, "Confirmation message was sent")

def send_order_confirmation_email(order: Order):
    subject = f"Order confirmation {order.id}"
    context = {"order" : order}
    text_context = render_to_string('email/confirmation email.txt', context)
    to_email = order.contact_email
    try:
        send_mail(subject, text_context, settings.DEFAULT_FROM_EMAIL, [to_email, settings.ADMIN_EMAIL])
    except Exception as e:
        print("Error sending email: {e}")