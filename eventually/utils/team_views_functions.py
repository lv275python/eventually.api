"""
Team view helper functions
================

This module provides helper functions for all Team's views functions.
"""
from authentication.models import CustomUser
from utils.validators import string_validator, list_of_int_validator


def find_users(members_id):
    """
    Function that have to find users in database.

    :param members_id: List of membes_id of team.
    :type members_id: List

    :return: list that contains members if they exist or None.
    """
    members = []
    for member_id in members_id:
        member = CustomUser.get_by_id(member_id)
        if member:
            members.append(member)
        else:
            return None
    return members


def create_team_dict(data, user):
    """
    Function that validate data for creating team and makes dict with valid data.

    :param data: dict that was got from json.
    :type data: dict

    :param user: user from request that creates team.
    :type user: CostomUser obj

    :return: dict needed for creating team obj if data currect or None.
    """
    result = {}
    result['owner'] = user

    members_id = data.get('members_id')
    if members_id:
        if list_of_int_validator(members_id):
            members = find_users(members_id)
            if not members:
                return None

        else:
            return None
    else:
        members = []
    members.append(user)
    if members:
        result['members'] = members
    name = data.get('name')
    if string_validator(name, 4, 30):
        result['name'] = name
    description = data.get('description')
    if string_validator(description, 0, 1024):
        result['description'] = description

    image = data.get('image')
    if string_validator(image, 0, 300):
        result['image'] = image
    return result


def get_users(data, user):
    """
    Function that have to find users that we want to remove or add in update method.

    :param data: dict that was got from json.
    :type data: dict

    :param user: user from request that creates team.
    :type user: CostomUser obj

    :return: tuple that contains users that we want to add or
    remove from team if they exist or None.
    """
    owner_id = data.get('owner_id')
    members_id_del = data.get('members_id_del')
    members_id_add = data.get('members_id_add')
    owner = CustomUser.get_by_id(owner_id) if isinstance(owner_id, int) else None

    if members_id_del:
        if list_of_int_validator(members_id_del):
            members_del = find_users(members_id_del)
            if not members_del or user in members_del or owner in members_del:
                return None
        else:
            return None
    else:
        members_del = None

    if members_id_add:
        if owner_id and isinstance(owner_id, int):
            members_id_add.append(owner_id)
        if list_of_int_validator(members_id_add):
            members_add = find_users(members_id_add)
            if not members_add:
                return None
        else:
            return None
    else:
        members_add = None
    return (owner, members_del, members_add)


def update_team_dict(data, user):
    """
    Function that validate data for updating team and makes dict with valid data.

    :param data: dict that was got from json.
    :type data: dict

    :param user: user from request that creates team.
    :type user: CostomUser obj

    :return: dict needed for updating team obj if data currect or None.
    """
    result = {}
    users = get_users(data, user)
    if users:
        (owner, members_del, members_add) = users
    else:
        return None
    result['owner'] = owner
    result['members_del'] = members_del
    result['members_add'] = members_add
    name = data.get('name')
    if string_validator(name, 4, 30):
        result['name'] = name
    description = data.get('description')
    if string_validator(description, 0, 1024):
        result['description'] = description
    image = data.get('image')
    if not (string_validator(image, 0, 300) or image is None):
        return None
    result['image'] = image
    return result
