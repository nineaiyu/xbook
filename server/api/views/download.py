#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xbook
# filename : download
# author : ly_13
# date : 2022/9/19

import logging

from django.http import HttpResponseRedirect, HttpResponseNotFound
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.models import AliyunFileInfo
from api.utils.drive import get_download_url
from api.utils.serializer import FileInfoSerializer
from common.core.filter import OwnerUserFilter
from common.core.response import ApiResponse

logger = logging.getLogger(__file__)


class DownloadView(ReadOnlyModelViewSet):
    queryset = AliyunFileInfo.objects.all()
    serializer_class = FileInfoSerializer
    filter_backends = [OwnerUserFilter]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        download_url = get_download_url(instance)
        logger.warning(download_url)
        if download_url:
            instance.downloads += 1
            instance.save(update_fields=['downloads'])
            return ApiResponse(**download_url)
        return ApiResponse(code=1001, msg='文件违规')

    def list(self, request, *args, **kwargs):
        return ApiResponse(code=1001, msg='获取失败')


class DirectlyDownloadView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, file_pk, file_id, file_name):
        instance = AliyunFileInfo.objects.filter(pk=file_pk, file_id=file_id).first()
        if instance:
            download_url_dict = get_download_url(instance)
            logger.warning(download_url_dict)
            if download_url_dict and download_url_dict.get('download_url'):
                instance.downloads += 1
                instance.save(update_fields=['downloads'])
                return HttpResponseRedirect(redirect_to=download_url_dict.get('download_url'))
        return HttpResponseNotFound(content="文件不存在")
