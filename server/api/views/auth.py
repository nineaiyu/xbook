#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xbook
# filename : auth
# author : ly_13
# date : 5/19/2023

# !/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xbook
# filename : userinfo
# author : ly_13
# date : 2022/9/13
from django.conf import settings
from django.contrib import auth
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.models import UserInfo
from api.utils.serializer import UserInfoSerializer, UserInfoUpdateSerializer
from common.core.response import ApiResponse
from common.utils.token import make_token, verify_token


def get_token_lifetime():
    access_token_lifetime = settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME')
    refresh_token_lifetime = settings.SIMPLE_JWT.get('REFRESH_TOKEN_LIFETIME')
    return {
        'access_token_lifetime': int(access_token_lifetime.total_seconds()),
        'refresh_token_lifetime': int(refresh_token_lifetime.total_seconds()),
    }


class LoginView(TokenObtainPairView):

    def get(self, request):
        token = make_token(request.query_params.get('client_id', 'xbook'), time_limit=180, force_new=True)
        data = {'token': token}
        data.update(get_token_lifetime())
        return ApiResponse(data=data)

    def post(self, request, *args, **kwargs):
        client_id = request.data.get('client_id')
        token = request.data.get('token')
        if client_id and token and verify_token(token, client_id, success_once=True):
            data = super().post(request, *args, **kwargs).data
            data.update(get_token_lifetime())
            return ApiResponse(data=data)
        return ApiResponse(code=9999, msg='token校验失败,请刷新页面重试')


class RefreshTokenView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        data = super().post(request, *args, **kwargs).data
        data.update(get_token_lifetime())
        return ApiResponse(data=data)


class UserInfoView(APIView):

    def get(self, request):
        data = UserInfoSerializer(request.user).data
        return ApiResponse(data=data)

    def put(self, request):
        serializer = UserInfoUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return ApiResponse()
        return ApiResponse(code=1001, msg='修改失败')


class LogoutView(APIView):

    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return ApiResponse()


class FingerprintLoginView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        data = request.data
        client_id = data.get('client_id')
        token = data.get('token')
        if verify_token(token, client_id, success_once=True):
            username = client_id
            password = client_id
            user = auth.authenticate(username=username, password=password, is_active=True)
            if not user:
                last_name = "1"
                first_name = f"会员_{username[:10]}"
                if username == password == client_id:
                    last_name = "0"
                    first_name = f"游客_{username[:10]}"
                user = UserInfo.objects.create_user(username=username, password=password, last_name=last_name,
                                                    first_name=first_name)
            refresh = RefreshToken.for_user(user)
            result = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            user.last_login = timezone.now()
            user.save(update_fields=["last_login"])
            result.update(**get_token_lifetime())
            return ApiResponse(data=result)
        return ApiResponse(code=9999, msg='token校验失败,请刷新页面重试')
