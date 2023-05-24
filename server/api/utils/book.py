#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : book
# author : ly_13
# date : 5/24/2023
from api.models import BookLabels, BookFileInfo
from common.base.magic import run_function_by_locker


def increase_grading_locker(*args, **kwargs):
    return f'increase_grading_locker_{args[0]}'


@run_function_by_locker(timeout=60, lock_func=increase_grading_locker)
def increase_grading(book_id, index):

    book = BookFileInfo.objects.filter(pk=book_id).first()
    b_c = BookLabels.get_grading().count()
    if index >= b_c:
        return
    grading = []
    for _, grade in zip(range(b_c), book.grading + [0] * (b_c - len(book.grading))):
        grading.append(grade)

    grading[index]+=1
    book.grading = grading
    book.save(update_fields=['grading'])
    return True