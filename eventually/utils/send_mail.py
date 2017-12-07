"""This is send mail method"""
from smtplib import SMTPRecipientsRefused
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_email(subject, message, recipient_list, template, ctx):
    """
    Function that provides message sending to the user

    :param subject: subject of email
    :type subject: string

    :param message: string with text message
    :type message: string

    :param recipient_list: list with users
    :type recipient_list: list

    :param template: string with title of template
    :type template: string

    :param ctx: set with parameters for html template
    :type ctx: set

    :return:
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    html_message = render_to_string('emails/' + template, ctx)
    try:
        send_mail(subject, message, from_email, recipient_list,
                  fail_silently=False, html_message=html_message)
    except SMTPRecipientsRefused:
        return False
    return True
