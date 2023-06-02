#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : clubhouse_robot
# filename : auth
# author : ly_13
# date : 1/20/2023

from django.http.cookie import parse_cookie
from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):

    def get_header(self, request):
        header = super().get_header(request)
        if not header:
            cookies = request.META.get('HTTP_COOKIE')
            if cookies:
                cookie_dict = parse_cookie(cookies)
                header = f"Bearer {cookie_dict.get('X-Token')}".encode('utf-8')
        return header
