#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xbook
# filename : serializer
# author : ly_13
# date : 5/19/2023

import logging

from rest_framework import serializers

from api import models

logger = logging.getLogger(__file__)


class AliyunDriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AliyunDrive
        exclude = ["owner_id", "access_token", "refresh_token"]
        read_only_fields = list(
            set([x.name for x in models.AliyunDrive._meta.fields]) - {"enable", "private", "description"})


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = ['username', 'first_name', 'email', 'last_login', 'last_name']
        read_only_fields = list(
            set([x.name for x in models.UserInfo._meta.fields]) - {"first_name"})

    first_name = serializers.SerializerMethodField()

    def get_first_name(self, obj):
        return obj.first_name if obj.first_name else obj.username


class UserInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = ['first_name', 'old_password', 'new_password']
        extra_kwargs = {
            "old_password": {"write_only": True},
            "new_password": {"write_only": True},
        }

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        old_password = validated_data.get("old_password")
        new_password = validated_data.get("new_password")
        if old_password and new_password and instance.last_name != "0":
            if not instance.check_password(validated_data.get("old_password")):
                raise Exception('旧密码校验失败')
            instance.set_password(validated_data.get("new_password"))
            instance.save()
            return instance
        return super(UserInfoUpdateSerializer, self).update(instance, validated_data)


class BookInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BookFileInfo
        exclude = ["owner_id"]
        read_only_fields = list(
            set([x.name for x in models.BookFileInfo._meta.fields]) - {"description"})


class FileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AliyunFileInfo
        exclude = ["owner_id", "aliyun_drive_id"]
        read_only_fields = list(
            set([x.name for x in models.AliyunFileInfo._meta.fields]) - {"description"})

    book = serializers.SerializerMethodField()

    def get_book(self, obj):
        return getattr(obj, 'bookfileinfo', {})
