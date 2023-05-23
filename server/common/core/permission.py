#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : robot_server
# filename : permission
# author : ly_13
# date : 5/8/2023
import re

from django.conf import settings
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


def get_user_permission(user_obj):
    # permission_data = UserPermissionCache(user_obj.pk)

    menu = []
    if user_obj.role:
        menu = user_obj.role.menu.filter(enable=True).values('api_route', 'method').all().distinct()
    return menu


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        auth = bool(request.user and request.user.is_authenticated)
        if auth:
            if request.user.is_superuser:
                return True
            url = request.path_info
            for w_url in settings.PERMISSION_WHITE_URL:
                if re.match(w_url, url):
                    return True
            permission_data = get_user_permission(request.user)
            for p_data in permission_data:
                if p_data.get('method') == request.method and re.match(p_data.get('api_route'), url):
                    return True
        raise PermissionDenied('权限不足')
