#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : lobby
# author : ly_13
# date : 5/24/2023
import json
import logging

from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from api.models import BookFileInfo, BookLabels
from api.utils.book import increase_grading, increase_downloads
from api.utils.drive import get_download_url
from api.utils.serializer import LobbyFileSerializer, BookCategorySerializer, BookDetailSerializer
from common.core.filter import OwnerUserFilter
from common.core.response import PageNumber, ApiResponse
from common.utils.token import verify_token

logger = logging.getLogger(__file__)


class BookLobbyView(APIView):
    permission_classes = []
    authentication_classes = []

    # @cache_response(timeout=600)
    def get(self, request):
        result = []
        queryset = BookFileInfo.objects.filter(publish=True).order_by('-created_time')[:10]
        data = LobbyFileSerializer(queryset, many=True, context={'time_limit': 600}).data
        result.append({'category': {'name': '最新发布', 'id': 0}, 'data': data})
        for l in BookLabels.get_categories().values('id', 'name').all():
            queryset = BookFileInfo.objects.filter(publish=True, categories__id=l['id']).order_by('-created_time')[:10]
            data = LobbyFileSerializer(queryset, many=True, context={'time_limit': 600}).data
            result.append({'category': l, 'data': data})
        return ApiResponse(data=result)


class BookCategoryFilter(filters.FilterSet):
    categories = filters.CharFilter(field_name='categories', method='categories_filter')

    def categories_filter(self, queryset, name, value):
        try:
            category = json.loads(value)
        except:
            category = []
        if category:
            lookup = '__'.join([name, 'in'])
            return queryset.filter(**{lookup: category}).distinct()
        else:
            return queryset

    class Meta:
        model = BookFileInfo
        fields = ['name']


class BookCategoryView(ReadOnlyModelViewSet):
    permission_classes = []
    authentication_classes = []

    queryset = BookFileInfo.objects.all()
    serializer_class = BookCategorySerializer
    pagination_class = PageNumber

    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['size', 'created_time', 'downloads']
    filterset_class = BookCategoryFilter

    def list(self, request, *args, **kwargs):
        data = super().list(request, *args, **kwargs).data
        return ApiResponse(data=data)


class BookDetailView(mixins.RetrieveModelMixin, GenericViewSet):
    permission_classes = []
    authentication_classes = []

    queryset = BookFileInfo.objects.all()
    serializer_class = BookDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        data = super().retrieve(request, *args, **kwargs).data
        return ApiResponse(data=data)

class LobbyAction(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        action = request.data.get('action', '')
        book_id = request.data.get('book_id', '')
        index = request.data.get('index')
        token = request.data.get('token')
        if verify_token(token, f"{book_id}", success_once=False):
            if action =='grading' and index is not None:
                grading_info = increase_grading(book_id, int(index))
                if grading_info:
                    return ApiResponse(grading_info=grading_info)
            if action == 'download':
                download_url = increase_downloads(book_id)
                if download_url:
                    return ApiResponse(**download_url)
        return ApiResponse(code=1001,msg='操作失败')