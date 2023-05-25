#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : book
# author : ly_13
# date : 5/24/2023
from api.models import BookLabels, BookFileInfo
from api.utils.drive import get_download_url
from api.utils.serializer import BookInfoSerializer
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
