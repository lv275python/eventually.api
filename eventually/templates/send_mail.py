"""This is send mail method"""
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from authentication.models import CustomUser
from team.models import Team
from event.models import Event


def send_email_update_password(user_id):
    """
    Function that provides message sending to the user in case he update his password

    :param user_id: user`s id
    :type user_id: int

    :return: True if function send mail, False in other cases
    """
    if user_id:
        user_id = CustomUser.get_by_id(user_id)
        ctx = {
            'first_name': user_id.first_name,
            'password': user_id.password
        }
        html_message = render_to_string('update_password.html', ctx)
        subject = 'New password'
        from_email = settings.DEFAULT_FROM_EMAIL
        message = 'Your password has changed'
        recipient_list = [user_id.email]
        send_mail(subject, message, from_email, recipient_list,
                  fail_silently=False, html_message=html_message)
        return True


def send_email_join_team(user_id, team_id):
    """
    Function that provides message sending to the user in case he was invited to a team

    :param team_id: team`s id
    :type team_id: int

    :param user_id: user`s id
    :type user_id: int

    :return: True if function send mail, False in other cases
    """
    if user_id and team_id:
        user_id = CustomUser.get_by_id(user_id)
        team_id = Team.get_by_id(team_id)
        ctx = {
            'first_name': user_id.first_name,
            'team_name': team_id.name
        }
        html_message = render_to_string('join_team.html', ctx)
        subject = 'Invite to a team'
        from_email = settings.DEFAULT_FROM_EMAIL
        message = 'You were invited to a team!'
        recipient_list = [user_id.email]
        send_mail(subject, message, from_email, recipient_list,
                  fail_silently=False, html_message=html_message)
        return True


def send_email_remind(user_id, event_id):
    """
    Function that provides message sending to the user to remind about smth event
    :param user_id: user`s id
    :type user_id: int

    :param event_id: event`s id
    :type event_id: int

    :return: True if function send mail, False in other cases
    """
    user_id = CustomUser.get_by_id(user_id)
    event_id = Event.get_by_id(event_id)
    ctx = {
        'first_name': user_id.first_name,
        'event_name': event_id.name
    }
    html_message = render_to_string('remind.html', ctx)
    subject = 'Today`s event'
    from_email = settings.DEFAULT_FROM_EMAIL
    message = 'You have event today'
    recipient_list = [user_id.email]
    send_mail(subject, message, from_email, recipient_list,
              fail_silently=False, html_message=html_message)
    return True
