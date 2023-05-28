#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : action
# author : ly_13
# date : 5/23/2023
from rest_framework.views import APIView

from api.models import AliyunFileInfo, BookFileInfo
from api.tasks import delay_refresh_lobby_cache
from api.utils.drive import batch_delete_file, batch_get_download_url
from common.core.response import ApiResponse


class ManyActionView(APIView):

    def post(self, request, name):
        action = request.data.get('action', '')
        if name == 'file':
            file_id_list = request.data.get('file_id_list', [])
            if action in ['delete', 'download'] and file_id_list:
                file_obj_list = AliyunFileInfo.objects.filter(owner_id=request.user, file_id__in=file_id_list).all()
                if file_obj_list:
                    if action == 'download':
                        return ApiResponse(data=batch_get_download_url(file_obj_list))
                    elif action == 'delete':
                        batch_delete_file(file_obj_list)
                        AliyunFileInfo.objects.filter(owner_id=request.user, file_id__in=file_id_list).delete()
                        return ApiResponse()
        if name == 'book':
            book_id_list = request.data.get('book_id_list', [])
            if action in ['delete', 'download'] and book_id_list:
                if action == 'delete':
                    BookFileInfo.objects.filter(owner_id=request.user, pk__in=book_id_list).delete()
                elif action == 'download':
                    file_obj_list = AliyunFileInfo.objects.filter(owner_id=request.user,
                                                                  bookfileinfo__pk__in=book_id_list).all()
                    return ApiResponse(data=batch_get_download_url(file_obj_list))
        if name == 'lobby':
            if action == 'cache':
                delay_refresh_lobby_cache()
                return ApiResponse()
        return ApiResponse(code=1001, msg='操作失败')
