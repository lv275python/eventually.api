"""This is test send mail method"""
from unittest import TestCase
from unittest import mock
from utils.send_mail import send_email
from smtplib import SMTPRecipientsRefused
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
    """

def raise_SMTPRecipientsRefused(*args, **kwargs):
    raise SMTPRecipientsRefused("testEmailFalse")

class TestEmail(TestCase):
    def testEmailTrue(self):

        ctx = {'first_name': "python"}
        subject = 'Pasword reset'
        message = 'Successful pasword reset.'
        recipient_list = ['python@hmail.com']
        template = 'update_password.html'
        with mock.patch('django.core.mail.send_mail') as mock_send_mail:
            mock_send_mail.return_value = None
            with mock.patch('django.template.loader.render_to_string') as mock_render_to_string:
                mock_render_to_string.return_value = "TEST_TEXT"
                param = send_email('stringa', 'stringa', recipient_list, template, ctx)
                self.assertTrue(param)

    @mock.patch('utils.send_mail.send_mail', raise_SMTPRecipientsRefused)
    def testEmailFalse(self):

        ctx = {'first_name': "python"}
        subject = 'Pasword reset'
        message = 'Successful pasword reset.'
        recipient_list = ['python@hmail.com']
        template = 'update_password.html'
        with mock.patch('django.template.loader.render_to_string') as mock_render_to_string:
            mock_render_to_string.return_value = "TEST_TEXT"
            param = send_email('stringa', 'stringa', recipient_list, template, ctx)
            self.assertFalse(param)
