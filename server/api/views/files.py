#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xbook
# filename : files
# author : ly_13
# date : 2022/9/18
import json
import logging

from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

from api.models import AliyunFileInfo
from api.utils.drive import get_aliyun_drive
from api.utils.serializer import FileInfoSerializer
from common.cache.storage import DownloadUrlCache
from common.core.filter import OwnerUserFilter
from common.core.modelset import BaseModelSet
from common.core.response import PageNumber, ApiResponse

logger = logging.getLogger(__file__)


class FileInfoFilter(filters.FilterSet):
    min_size = filters.NumberFilter(field_name="size", lookup_expr='gte')
    max_size = filters.NumberFilter(field_name="size", lookup_expr='lte')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    bookinfo = filters.CharFilter(field_name='bookinfo', method='bookinfo_filter')

    def bookinfo_filter(self, queryset, name, value):
        return queryset.exclude(bookfileinfo__isnull=bool(json.loads(value)))

    class Meta:
        model = AliyunFileInfo
        fields = ['name']


class FileInfoView(BaseModelSet):
    queryset = AliyunFileInfo.objects.all()
    serializer_class = FileInfoSerializer
    pagination_class = PageNumber

    filter_backends = [OwnerUserFilter, filters.DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['size', 'created_at', 'downloads']
    filterset_class = FileInfoFilter

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        ali_obj = get_aliyun_drive(instance.aliyun_drive_id)
        result = ali_obj.move_file_to_trash(instance.file_id)
        DownloadUrlCache(instance.drive_id, instance.file_id).del_storage_cache()
        logger.debug(f'{instance.aliyun_drive_id} move {instance} to trash.result:{result}')
        self.perform_destroy(instance)
        return ApiResponse()

    def create(self, request, *args, **kwargs):
        return ApiResponse(code=1001, msg='添加失败')


