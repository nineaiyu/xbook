#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : robot_server
# filename : utils
# author : ly_13
# date : 5/9/2023
from collections import OrderedDict

from django.urls import URLPattern, URLResolver


def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    """递归去获取URL
    :param pre_namespace: namespace前缀，以后用户拼接name
    :param pre_url: url前缀，以后用于拼接url
    :param urlpatterns: 路由关系列表
    :param url_ordered_dict: 用于保存递归中获取的所有路由
    """
    for item in urlpatterns:
        if isinstance(item, URLPattern):
            if not item.name:
                continue

            if pre_namespace:
                name = "%s:%s" % (pre_namespace, item.name)
            else:
                name = item.name
            if not item.name:
                raise Exception('URL路由中必须设置name属性')
            url = pre_url + item.pattern.regex.pattern.lstrip('^')
            # url = url.replace('^', '').replace('$', '')
            url_ordered_dict[name] = {'name': name, 'url': url}

        elif isinstance(item, URLResolver):  # 路由分发，递归操作
            if pre_namespace:
                if item.namespace:
                    namespace = "%s:%s" % (pre_namespace, item.namespace)
                else:
                    namespace = item.namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None

            recursion_urls(namespace, pre_url + item.pattern.regex.pattern.lstrip('^'), item.url_patterns,
                           url_ordered_dict)


def get_all_url_dict(urlpatterns, pre_url='/'):
    """
       获取项目中所有的URL（必须有name别名）
    """
    url_ordered_dict = OrderedDict()
    url_ordered_dict['#'] = {'name': '#', 'url': '#'}
    recursion_urls(None, pre_url, urlpatterns, url_ordered_dict)  # 递归去获取所有的路由
    return url_ordered_dict.values()
