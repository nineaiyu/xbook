#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xbook
# filename : auth
# author : ly_13
# date : 1/20/2023

import base64

from django.http.cookie import parse_cookie
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from api.models import UserInfo
from common.cache.storage import UserTokenCache


def get_cookie_token(request):
    cookies = request.META.get('HTTP_COOKIE')
    if cookies:
        cookie_dict = parse_cookie(cookies)
        return cookie_dict.get('X-Token')


def get_user_from_request_auth(request_token):
    if request_token:
        try:
            format_token = base64.b64decode(request_token).decode()
            user_name = format_token.split(":")[0]
            auth_token = format_token.split(":")[1]
        except Exception:
            raise AuthenticationFailed({"code": 1001, "detail": "token 异常"})

        if not auth_token:
            raise AuthenticationFailed({"code": 1001, "detail": "token 缺失"})

        auth_cache = UserTokenCache(auth_token)
        userinfo = auth_cache.get_storage_cache()
        if not userinfo:
            raise AuthenticationFailed({"code": 1001, "detail": "token 失效"})
        if user_name != userinfo.get('username', None):
            raise AuthenticationFailed({"code": 1001, "detail": "token 无效"})

        user_obj = UserInfo.objects.filter(pk=userinfo.get('pk', None),
                                           username=userinfo.get("username")).first()
        if not user_obj:
            raise AuthenticationFailed({"code": 1001, "detail": "用户异常"})
        if user_obj.is_active:
            auth_cache.set_storage_cache(userinfo, 3600 * 24 * 7)
            return user_obj, auth_token
        else:
            raise AuthenticationFailed({"code": 1001, "detail": "用户禁用"})
    else:
        raise AuthenticationFailed({"code": 1002, "detail": "认证无效"})


class TokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        if request.method == "OPTIONS":
            return None
        request_token = request.META.get("HTTP_AUTHORIZATION",
                                         request.META.get("HTTP_X_TOKEN",
                                                          request.query_params.get("token", get_cookie_token(request))))
        return get_user_from_request_auth(request_token)


class WebSocketAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        """
        Instantiate a session wrapper for this scope, resolve the session and
        call the inner application.
        """
        token = scope.get('query_string')
        print(token)
        try:
            user_obj, auth_token = get_user_from_request_auth(token)

        except Exception as e:
            print(e)

        return await self.inner(scope, receive, send)
