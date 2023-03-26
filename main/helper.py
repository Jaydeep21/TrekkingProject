
from django.core.mail import send_mail

from django.conf import settings 
from .models import EnrolledHikers
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

def send_forget_password_mail(email , reset_url ):
    subject = 'Your forget password link'
    message = f'Hi , click on the link to reset your password {reset_url}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

def email(request, id, cancellation):
    hike = EnrolledHikers.objects.get(pk=id)
    hike.cancellation = cancellation
    tx = float("{:.2f}".format(hike.hike.cost * .13))
    total = tx + hike.hike.cost
    htmly = get_template('email.html')
    if hike.cancellation:
        subject, from_email, to = 'Booking Cancellation', 'from@example.com', request.user.email
    else:
        subject, from_email, to = 'Booking Confirmation', 'from@example.com', request.user.email
    html_content = htmly.render({"hike": hike, "tax": tx, "total":total })
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.content_subtype = "html"
    msg.send()