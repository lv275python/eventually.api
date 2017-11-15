from django.http import HttpResponse
from eventually.settings import FRONT_HOST
from utils.jwttoken import create_token
from utils.send_mail import send_email


def send_reseting_letter(user):
    """
    Function that provides sending reset password letter to user.

    :param user: user that we want send letter to.
    :type user: CustoUser obj

    :return: HttpResponse with status 200.
    """
    arg = {'user_id': user.id}
    token = create_token(data=arg, expiration_time=60 * 60)
    ctx = {'first_name': user.first_name,
           'token': token,
           'domain': FRONT_HOST}
    subject = 'Pasword reset'
    message = 'You tried to change your password.'
    recipient_list = [user.email]
    template = 'change_password_link.html'
    send_email(subject, message, recipient_list, template, ctx)
    return HttpResponse(status=200)


def reset_pasword(user, new_password):
    """
    Function that provides reseting password.

    :param user: user that wants to reset password.
    :type user: CustoUser obj

    :param new_password: New_password
    :type new_password: str

    :return: HttpResponse with status 200.
    """
    user.password = new_password
    user.save()
    ctx = {'first_name': user.first_name}
    subject = 'Pasword reset'
    message = 'Successful pasword reset.'
    recipient_list = [user.email]
    template = 'update_password.html'
    send_email(subject, message, recipient_list, template, ctx)
    return HttpResponse(status=200)
