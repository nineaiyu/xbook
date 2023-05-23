#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xbook
# filename : book
# author : ly_13
# date : 5/19/2023
import logging

from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

from api.models import BookFileInfo
from api.utils.serializer import BookInfoSerializer
from common.core.filter import OwnerUserFilter
from common.core.modelset import BaseModelSet
from common.core.response import PageNumber

logger = logging.getLogger(__file__)


class BookInfoFilter(filters.FilterSet):
    min_size = filters.NumberFilter(field_name="size", lookup_expr='gte')
    max_size = filters.NumberFilter(field_name="size", lookup_expr='lte')
    introduction = filters.CharFilter(field_name='introduction', lookup_expr='icontains')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    author = filters.CharFilter(field_name='author', lookup_expr='icontains')

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
