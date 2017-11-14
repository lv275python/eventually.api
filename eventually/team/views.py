"""
Views module
============
"""

import json
from json.decoder import JSONDecodeError
from django.http import JsonResponse, HttpResponse
from django.views.generic.base import View
from .models import Team
from authentication.models import CustomUser
from utils.utils import json_loads
from utils.validators import string_validator, required_keys_validator, list_of_int_validator


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
        data['teams'] = [a_team.to_dict() for a_team in teams]
        return JsonResponse(data, status=200)

    def post(self, request):
        """Handles POST request."""

        data = json_loads(request.body)
        keys_required = ['members_id',
                         'owner_id',
                         'name', 
                         'description', 
                         'image']
        data_valid = required_keys_validator(data, keys_required, strict=False)
        if data_valid:
            errors = {'member_ids': set()}
            members_id = data.get('members_id')
            if list_of_int_validator(members_id):
                members = []
                for member_id in members_id:
                    member = CustomUser.get_by_id(member_id)
                    if member:
                        members.append(member)
                    else:
                        errors['member_ids'].add(member_id)
            else:
                errors = {'message' 'Unvalid members_id list'}
                return JsonResponse(status=400, data=errors)
            owner_id = data.get('owner_id')
            if isinstance(owner_id, int):
                owner = CustomUser.get_by_id(owner_id)
            else:
                errors = {'message' 'Unvalid owner_id'}
                return JsonResponse(status=400, data=errors)
            if not owner:
                errors['member_ids'].add(owner_id)
            name = data.get('name')
            if not string_validator(name, min_length=4):
                errors = {'message': 'Unvalid name'}
                return JsonResponse(status=400, data=errors)
            description = data.get('description')
            if not string_validator(description):
                errors = {'message': 'Unvalid description'}
                return JsonResponse(status=400, data=errors)
            image = data.get('image')
            if not string_validator(image):
                errors = {'message': 'Unvalid image'}
                return JsonResponse(status=400, data=errors)
            errors['member_ids'] = list(errors['member_ids'])
            if errors['member_ids']:
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
            errors = {'message': 'validation is failed'}
            return JsonResponse(status=400, data=errors)

    def put(self, request, team_id=None):
        """Handles PUT request."""

        if team_id:
            team = Team.get_by_id(team_id)
            if team:
                data = json_loads(request.body)
                errors = {'member_ids': set()}
                members_id = data.get('members_id')
                if list_of_int_validator(members_id):
                    members = []
                    for member_id in members_id:
                        member = CustomUser.get_by_id(member_id)
                        if member:
                            members.append(member)
                        else:
                            errors['team']['member_ids'].add(member_id)
                else:
                    errors = {'message' 'Unvalid members_id list'}
                    return JsonResponse(status=400, data=errors)
                owner_id = data.get('owner_id')
                if isinstance(owner_id, int):
                    owner = CustomUser.get_by_id(owner_id)
                else:
                    errors = {'message' 'Unvalid owner_id'}
                    return JsonResponse(status=400, data=errors)
                if not owner:
                    errors['team']['member_ids'].add(owner_id)
                name = data.get('name')
                if not (string_validator(name) or name is None):
                    errors = {'message': 'Unvalid name'}
                    return JsonResponse(status=400, data=errors)
                description = data.get('description')
                if not (string_validator(description) or description is None):
                    errors = {'message': 'Unvalid description'}
                    return JsonResponse(status=400, data=errors)
                image = data.get('image')
                if not (string_validator(image) or image is None):
                    errors = {'message': 'Unvalid image'}
                    return JsonResponse(status=400, data=errors)
                errors['member_ids'] = list(errors['member_ids'])
                if errors['member_ids']:
                    return JsonResponse(status=400, data=errors)
                data = {
                    'owner': owner,
                    'members': members,
                    'name': name,
                    'description': description,
                    'image': image,
                }
                team.update(**data)
                team = team.to_dict()
                return JsonResponse(team, status=201)
            return HttpResponse(status=404)
        return HttpResponse(status=400)

    def delete(self, request, team_id=None):
        """Handles DELETE request."""

        if team_id:
            is_deleted = Team.delete_by_id(team_id)
            if is_deleted:
                return HttpResponse(status=200)
        return HttpResponse(status=400)
