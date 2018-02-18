"""
Cache helper
=============
The module that provides functionality for deleting cache afer data changes.
"""

from django.core.cache import cache
from authentication.models import CustomUser
from event.models import Event
from team.models import Team


def del_cache_team(team_id):
    """
    Deletes cache for teams after team edit for all team members.
    """
    team = Team.get_by_id(team_id)
    team = team.to_dict()
    members = team['members_id']
    for member in members:
        hash_teams_key = 'all_teams_{0}'.format(member)
        cache.delete(hash_teams_key)
    return False

def del_cache_events(event_id):
    """
    Deletes cache for event after event edit for all event`s team members.
    """
    event = Event.get_by_id(event_id)
    team = event.team
    team = team.to_dict()
    members = team['members_id']
    for member in members:
        hash_events_key = 'all_events_{0}'.format(member)
        cache.delete(hash_events_key)
    return True

def del_cache_profile(profile_id):
    """
    Deletes cache for custom profile after profile edit
    """
    custom_profile = CustomUser.get_by_id(profile_id)
    hash_profile_key = 'current_profile_{0}'.format(custom_profile)
    cache.delete(hash_profile_key)
    return True
