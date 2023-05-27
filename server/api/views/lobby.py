#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : lobby
# author : ly_13
# date : 5/24/2023
import json
import logging
import time

from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from api.models import BookFileInfo, BookLabels
from api.utils.book import increase_grading, increase_downloads, get_rank_list
from api.utils.serializer import LobbyFileSerializer, BookCategorySerializer, BookDetailSerializer
from common.cache.storage import GradingCache
from common.core.response import PageNumber, ApiResponse
from common.core.throttle import Download2Throttle, Download1Throttle
from common.utils.token import verify_token

logger = logging.getLogger(__file__)


class BookCategoriesView(APIView):
    permission_classes = []
    authentication_classes = []

    # @cache_response(timeout=600)
    def get(self, request):
        act = request.query_params.get('act', '')
        if act == 'lobby':
            result = [{'id': 0, 'name': '首页'}, {'id': -1, 'name': '排行榜'}]
        elif act == 'rank':
            result = [{'id': -1, 'name': '总排行榜'}]
        else:
            result = []
        for l in BookLabels.get_categories().order_by('created_time').values('id', 'name').all():
            result.append(l)

        search_choices = [
            {'label': '书籍名', 'value': 'book'},
            {'label': '作者', 'value': 'author'},
            {'label': '标签', 'value': 'tags'},
            {'label': '发布者', 'value': 'publisher'},
        ]

        return ApiResponse(data=result, search_choices=search_choices)


class BookLobbyView(APIView):
    permission_classes = []
    authentication_classes = []

    # @cache_response(timeout=600)
    def get(self, request):
        result = []
        limit = 10
        queryset = BookFileInfo.objects.filter(publish=True).order_by('-created_time')[:limit]
        data = LobbyFileSerializer(queryset, many=True).data
        result.append({'category': {'id': 0, 'name': '最新发布'}, 'data': data})
        for l in BookLabels.get_categories().order_by('created_time').values('id', 'name').all():
            queryset = BookFileInfo.objects.filter(publish=True, categories__id=l['id']).order_by('-created_time')[
                       :limit]
            data = LobbyFileSerializer(queryset, many=True).data
            result.append({'category': l, 'data': data})
        return ApiResponse(data=result)


class BookRankDataView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request):
        try:
            category = json.loads(request.query_params.get('categories'))
            category = [x for x in category if x > 0]
        except:
            category = []
        try:
            limit = int(request.query_params.get('limit'))
            if limit not in range(10, 30):
                raise
        except:
            limit = 10
        return ApiResponse(rank_data=get_rank_list(category, limit))


class BookCategoryFilter(filters.FilterSet):
    categories = filters.CharFilter(field_name='categories', method='categories_filter')
    search = filters.CharFilter(field_name='search', method='search_filter')

    def search_filter(self, queryset, name, value):
        try:
            search = json.loads(value)
        except:
            search = {}
        act = search.get('act', '')
        key = search.get('key', '')
        if act and key:
            if act == 'book':
                return queryset.filter(name__icontains=key).distinct()
            elif act == 'author':
                return queryset.filter(author__icontains=key).distinct()
            elif act == 'tags':
                return queryset.filter(tags__name__icontains=key, tags__label_type=1).distinct()
            elif act == 'publisher':
                return queryset.filter(owner_id__first_name__icontains=key).distinct()
            elif act == 'pid':
                return queryset.filter(owner_id__username=key).distinct()
            elif act == 'tid':
                return queryset.filter(tags__id=key).distinct()
        return queryset.filter(Q(name__icontains=value) | Q(author__icontains=value)).distinct()

    def categories_filter(self, queryset, name, value):
        try:
            category = json.loads(value)
        except:
            category = []
        if category:
            if isinstance(category, list):
                lookup = '__'.join([name, 'in'])
            else:
                lookup = name
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
    throttle_classes = [Download1Throttle, Download2Throttle]
    def post(self, request):
        action = request.data.get('action', '')
        book_id = request.data.get('book_id', '')
        index = request.data.get('index')
        token = request.data.get('token')
        client_id = request.data.get('key')
        if verify_token(token, f"{book_id}", success_once=False):
            if action == 'grading' and index is not None:
                g_cache = GradingCache(book_id, client_id)
                if g_cache.get_storage_cache():
                    return ApiResponse(code=1001, msg='你已经评价过了，请明天再试')
                grading_info = increase_grading(book_id, int(index))
                if grading_info:
                    g_cache.set_storage_cache(time.time())
                    return ApiResponse(grading_info=grading_info)
            if action == 'download':
                download_url = increase_downloads(book_id)
                if download_url:
                    return ApiResponse(**download_url)
        else:
            return ApiResponse(code=1001, msg='授权失效，请刷新页面重试')
        return ApiResponse(code=1001, msg='数据异常，操作失败')
