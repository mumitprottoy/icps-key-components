from django.core.mail import send_mail, get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import smtplib
from icps.settings import *
from django.contrib.auth.models import User
from .creds import emails
#===============================================================

# methods




def _send(message, fail_silently=False):
    with get_connection(
        host=EMAIL_HOST, 
        port=EMAIL_PORT, 
        username=message['creds']['email'], 
        password=message['creds']['password'], 
        use_tls=EMAIL_USE_TLS
        ) as connection:
        return send_mail(
            message['subject'], 
            message['plain'], 
            message['creds']['email'],
            message['to'], 
            html_message=message['html'],
            connection=connection,
            fail_silently=fail_silently)
        #connection.close()





    
def send_template_email(email_type, email, fail_silently=False, context={}):
    if email is not list: email=[email]
    subject = emails[email_type]['subject']
    html = render_to_string(emails[email_type]['html'], context)
    plain = strip_tags(html)
    message = {
        'creds': {
            'email':emails[email_type]['email'],
            'password':emails[email_type]['password'],
        },
        'to':email,
        'subject': subject,
        'html': html,
        'plain': plain 
    }
    return _send(message, fail_silently=fail_silently)
    