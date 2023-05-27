#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xbook
# filename : throttle
# author : ly_13
# date : 2022/9/13


from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class UploadThrottle(UserRateThrottle):
    """上传速率限制"""
    scope = "upload"


class Download1Throttle(AnonRateThrottle):
    """下载速率限制"""
    scope = "download1"


class Download2Throttle(AnonRateThrottle):
    """下载速率限制"""
    scope = "download2"
