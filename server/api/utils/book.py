#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : book
# author : ly_13
# date : 5/24/2023
import datetime

from django.utils import timezone

from api.models import BookLabels, BookFileInfo
from api.utils.drive import get_download_url
from api.utils.serializer import BookInfoSerializer, LobbyFileSerializer
from common.base.magic import run_function_by_locker


def increase_grading_locker(*args, **kwargs):
    return {'locker_key': f'increase_grading_locker_{args[0]}'}


@run_function_by_locker(timeout=60, lock_func=increase_grading_locker)
def increase_grading(book_id, index):
    book = BookFileInfo.objects.filter(pk=book_id).first()
    if not book:
        return
    b_c = BookLabels.get_grading().count()
    if index >= b_c:
        return
    grading = []
    for _, grade in zip(range(b_c), book.grading + [0] * (b_c - len(book.grading))):
        grading.append(grade)

    grading[index] += 1
    book.grading = grading
    book.save(update_fields=['grading'])
    return BookInfoSerializer().get_grading_info(book)


def increase_downloads_locker(*args, **kwargs):
    return {'locker_key': f'increase_downloads_locker_{args[0]}'}


@run_function_by_locker(timeout=30, lock_func=increase_downloads_locker)
def increase_downloads(book_id):
    book = BookFileInfo.objects.filter(pk=book_id).first()
    if not book:
        return
    download_url = get_download_url(book.file)
    if download_url:
        book.downloads += 1
        book.save(update_fields=['downloads'])
        return download_url


def get_rank_list(categories=None, limit=10):
    result = []
    rank_days = {
        0: '总',
        7: '周',
        30: '月',
        120: '季',
        360: '年',
    }
    for day, label in rank_days.items():
        queryset = BookFileInfo.objects.filter(publish=True)
        book_labels = []
        if categories:
            queryset = queryset.filter(categories__id__in=categories)
            book_labels = BookLabels.get_categories().filter(id__in=categories).values('name')
        if day != 0:
            default_timezone = timezone.get_default_timezone()
            value = timezone.make_aware(datetime.datetime.now() - datetime.timedelta(days=day), default_timezone)
            queryset = queryset.filter(created_time__gt=value)
        queryset = queryset.order_by('-created_time').order_by('-downloads')[:limit]
        data = LobbyFileSerializer(queryset, many=True).data
        result.append(
            {'category': {'id': day, 'name': f"{'-'.join([x['name'] for x in book_labels])}书籍{label}排行榜"},
             'data': data})
    return result
