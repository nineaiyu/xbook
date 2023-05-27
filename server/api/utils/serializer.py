#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xbook
# filename : serializer
# author : ly_13
# date : 5/19/2023

import logging

from rest_framework import serializers

from api import models
from common.utils.token import make_token

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
        fields = ['username', 'first_name', 'email', 'last_login', 'last_name', 'is_superuser']
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

    def validate(self, attrs):
        attrs['first_name'] = attrs['first_name'][:8]
        return attrs

    def update(self, instance, validated_data):
        old_password = validated_data.get("old_password")
        new_password = validated_data.get("new_password")
        if old_password and new_password:
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
        read_only_fields = ['owner_id_id', 'id', 'size', 'cover']

    file_info = serializers.SerializerMethodField()
    tags_info = serializers.SerializerMethodField()
    grading_info = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)

    def get_category(self, obj):
        return obj.categories.name

    def get_grading_info(self, obj):
        label_list = BookTagsSerializer(models.BookLabels.get_grading(), many=True).data
        result = []
        for label, grade in zip(label_list, obj.grading + [0] * (len(label_list) - len(obj.grading))):
            result.append({'label': label['label'], 'value': grade})
        return result

    def get_tags_info(self, obj):
        if not obj.tags:
            return []
        return BookTagsSerializer(obj.tags, many=True).data

    def get_file_info(self, obj):
        return {'id': obj.file.id, 'file_id': obj.file.file_id, 'name': obj.name}

    def validate(self, attrs):
        attrs['owner_id_id'] = self.context.get('request').user.pk
        attrs['size'] = attrs['file'].size
        return attrs


class FileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AliyunFileInfo
        exclude = ["owner_id", "aliyun_drive_id"]
        read_only_fields = list(
            set([x.name for x in models.AliyunFileInfo._meta.fields]) - {"description"})

    book = serializers.SerializerMethodField()

    def get_book(self, obj):
        book = getattr(obj, 'bookfileinfo', None)
        if book:
            return BookInfoSerializer(book).data
        return {}


class BookTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BookLabels
        fields = ['value', 'label']
        read_only_fields = list(set([x.name for x in models.UserInfo._meta.fields]))

    value = serializers.IntegerField(source='id')
    label = serializers.CharField(source='name')


class LobbyFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BookFileInfo
        fields = ['id', 'name', 'created_time', 'author']
        read_only_fields = list(set([x.name for x in models.UserInfo._meta.fields]))


class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BookFileInfo
        fields = ['id', 'name', 'created_time', 'author', 'tags_info', 'category', 'downloads', 'size', 'introduction',
                  'publisher']
        read_only_fields = list(set([x.name for x in models.UserInfo._meta.fields]))

    tags_info = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)
    publisher = serializers.SerializerMethodField()

    def get_publisher(self, obj):
        return {
            'first_name': obj.owner_id.first_name,
            'username': obj.owner_id.username
        }

    def get_category(self, obj):
        return obj.categories.name

    def get_tags_info(self, obj):
        if not obj.tags:
            return []
        return BookTagsSerializer(obj.tags, many=True).data


class BookDetailSerializer(BookCategorySerializer, BookInfoSerializer):
    class Meta:
        model = models.BookFileInfo
        fields = ['id', 'name', 'created_time', 'author', 'tags_info', 'category', 'downloads', 'size', 'introduction',
                  'token', 'grading_info', 'publisher', 'cover']
        read_only_fields = list(set([x.name for x in models.UserInfo._meta.fields]))

    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        context = self.context
        time_limit = context.get('time_limit', 600)
        prefix = context.get('prefix', 'lobby')
        return make_token(key=f"{obj.pk}", time_limit=time_limit, force_new=True, prefix=prefix)
