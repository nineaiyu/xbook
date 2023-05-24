#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xbook
# filename : book
# author : ly_13
# date : 5/19/2023
import json
import logging

from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView

from api.models import BookFileInfo, BookLabels
from api.utils.serializer import BookInfoSerializer, BookTagsSerializer
from common.core.filter import OwnerUserFilter
from common.core.modelset import BaseModelSet
from common.core.response import PageNumber, ApiResponse

logger = logging.getLogger(__file__)


class BookInfoFilter(filters.FilterSet):
    min_size = filters.NumberFilter(field_name="size", lookup_expr='gte')
    max_size = filters.NumberFilter(field_name="size", lookup_expr='lte')
    introduction = filters.CharFilter(field_name='introduction', lookup_expr='icontains')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    author = filters.CharFilter(field_name='author', lookup_expr='icontains')
    publish = filters.CharFilter(field_name='publish', method='publish_filter')
    categories = filters.CharFilter(field_name='categories', method='categories_filter')
    tags = filters.CharFilter(field_name='tags', method='categories_filter')

    def publish_filter(self, queryset, name, value):
        return queryset.filter(publish=bool(json.loads(value)))

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


class BookInfoView(BaseModelSet):
    queryset = BookFileInfo.objects.all()
    serializer_class = BookInfoSerializer
    pagination_class = PageNumber

    filter_backends = [OwnerUserFilter, filters.DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['size', 'created_at', 'downloads']
    filterset_class = BookInfoFilter

    def create(self, request, *args, **kwargs):
        data = super().create(request, *args, **kwargs)
        return ApiResponse(**data.data)

    def retrieve(self, request, *args, **kwargs):
        data = super().retrieve(request, *args, **kwargs)
        return ApiResponse(**data.data, )


class BookLabelInfoView(APIView):

    def get(self, request):
        l_type = request.query_params.get('l_type')
        l_type_list = []

        try:
            if l_type:
                l_type_list = json.loads(l_type)
        except:
            pass
        result = {}
        while len(l_type_list):
            l_type = l_type_list.pop()
            if l_type == 1:
                result['book_tags'] = BookTagsSerializer(BookLabels.get_tags(), many=True).data
            elif l_type == 2:
                result['book_categories'] = BookTagsSerializer(BookLabels.get_categories(), many=True).data
            elif l_type == 3:
                result['book_grading'] = BookTagsSerializer(BookLabels.get_grading(), many=True).data
            else:
                pass
        return ApiResponse(**result)
