"""
Views module
============
"""

import json
from django.http import JsonResponse, HttpResponse
from django.views.generic.base import View
from .models import Team
from authentication.models import CustomUser
from json.decoder import JSONDecodeError


class TeamView(View):
    """Team view handles GET, POST, PUT, DELETE requests.
    """

    def get(self, request, team_id=None):
        """Handles GET request."""

        if team_id:
            team = Team.get_by_id(team_id)
            if team:
                team = team.to_dict()
                return JsonResponse(team, status=200)
            return HttpResponse(status=404)

        teams = team.get_all()
        data = {}
        data['teams'] = [teama.to_dict() for teama in teams]

        return JsonResponse(data, status=200)

    def post(self, request):
        ##################################################
        #dont forget about user authentication validation#
        ##################################################
        """Handles POST request."""

        errors = {'team': {}}
        try:
            data = json.loads(request.body.decode('utf-8'))
        except JSONDecodeError:
            errors['team'].update({'JSON': 'JSON parse error'})
            return JsonResponse(status=400, data=errors)

        data_valid = data

        if data_valid:

            errors['team'].update({'member_ids': set()})
            members_id = data_valid.get('members_id')
            members = []
            for member_id in members_id:
                member = CustomUser.get_by_id(member_id)
                if member:
                    members.append(member)
                else:
                    errors['team']['member_ids'].add(member_id)

            owner_id = data_valid.get('owner_id')
            owner = CustomUser.get_by_id(owner_id)
            if not owner:
                errors['team']['member_ids'].add(owner_id)
            name = data_valid.get('name')
            description = data_valid.get('description')
            image = data_valid.get('image')

            errors['team']['member_ids'] = list(errors['team']['member_ids'])
            if errors['team']['member_ids']:
                return JsonResponse(status=400, data=errors)

            data = {
                'owner': owner,
                'members': members,
                'name': name,
                'description': description,
                'image': image,
            }

            team = Team.create(**data)
            team = team.to_dict()
            return JsonResponse(team, status=201)
        else:
            errors['team'].update({'validation': 'is failed'})
            return JsonResponse(status=400, data=errors)

    def put(self, request, team_id=None):
        ##################################################
        #dont forget about user authentication validation#
        ##################################################
        """Handles PUT request."""

        if team_id:
            team = Team.get_by_id(team_id)
            if team:
                errors = {'team': {}}
                try:
                    data = json.loads(request.body.decode('utf-8'))
                except JSONDecodeError:
                    errors['team'].update({'JSON': 'JSON parse error'})
                    return JsonResponse(status=400, data=errors)

                data_valid = data

                if data_valid:

                    errors['team'].update({'member_ids': set()})
                    members_id = data_valid.get('members_id')
                    members = []
                    for member_id in members_id:
                        member = CustomUser.get_by_id(member_id)
                        if member:
                            members.append(member)
                        else:
                            errors['team']['member_ids'].add(member_id)

                    owner_id = data_valid.get('owner_id')
                    owner = CustomUser.get_by_id(owner_id)
                    if not owner:
                        errors['team']['member_ids'].add(owner_id)
                    name = data_valid.get('name')
                    description = data_valid.get('description')
                    image = data_valid.get('image')

                    errors['team']['member_ids'] = list(errors['team']['member_ids'])
                    if errors['team']['member_ids']:
                        return JsonResponse(status=400, data=errors)

                    data = {
                        'owner': owner,
                        'members': members,
                        'name': name,
                        'description': description,
                        'image': image,
                    }

                    team = Team.create(**data)
                    team = team.to_dict()
                    return JsonResponse(team, status=201)
                else:
                    errors['team'].update({'validation': 'is failed'})
                    return JsonResponse(status=400, data=errors)

            return HttpResponse(status=404)

        return HttpResponse(status=400)

    def delete(self, request, team_id=None):
        """Handles DELETE request."""

        if team_id:
            is_deleted = Team.delete_by_id(team_id)
            if is_deleted:
                return HttpResponse(status=200)

        return HttpResponse(status=400)