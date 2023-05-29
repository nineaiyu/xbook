#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xbook
# filename : storage
# author : ly_13
# date : 2022/9/17
import logging

from django.core.cache import cache

from xbook.settings import CACHE_KEY_TEMPLATE

logger = logging.getLogger(__name__)


class RedisCacheBase(object):
    def __init__(self, cache_key, timeout=600):
        self.cache_key = cache_key
        self._timeout = timeout

    def __getattribute__(self, item):
        if isinstance(item, str) and item != 'cache_key':
            if hasattr(self, "cache_key"):
                logger.debug(f'act:{item} cache_key:{super().__getattribute__("cache_key")}')
        return super().__getattribute__(item)

    def get_storage_cache(self, defaults=None):
        return cache.get(self.cache_key, defaults)

    def get_storage_key_and_cache(self):
        return self.cache_key, cache.get(self.cache_key)

    def set_storage_cache(self, value, timeout=0):
        if isinstance(timeout, int) and timeout == 0:
            timeout = self._timeout
        return cache.set(self.cache_key, value, timeout)

    def append_storage_cache(self, value, timeout=None):
        with cache.lock(f"{self.cache_key}_lock", timeout=60, blocking_timeout=60):
            data = cache.get(self.cache_key, [])
            data.append(value)
            return cache.set(self.cache_key, data, timeout if timeout else self._timeout)

    def del_storage_cache(self):
        return cache.delete(self.cache_key)

    def incr(self, amount=1):
        return cache.incr(self.cache_key, amount)

    def expire(self, timeout):
        return cache.expire(self.cache_key, timeout=timeout)

    def iter_keys(self):
        if not self.cache_key.endswith('*'):
            self.cache_key = f"{self.cache_key}*"
        return cache.iter_keys(self.cache_key)

    def get_many(self):
        return cache.get_many(self.cache_key)

    def del_many(self):
        for delete_key in cache.iter_keys(self.cache_key):
            cache.delete(delete_key)
        return True


class TokenManagerCache(RedisCacheBase):
    def __init__(self, key, release_id):
        self.cache_key = f"{CACHE_KEY_TEMPLATE.get('make_token_key')}_{key.lower()}_{release_id}"
        super().__init__(self.cache_key)


class PendingStateCache(RedisCacheBase):
    def __init__(self, locker_key):
        self.cache_key = f"{CACHE_KEY_TEMPLATE.get('pending_state_key')}_{locker_key}"
        super().__init__(self.cache_key)


class UploadPartInfoCache(RedisCacheBase):
    def __init__(self, locker_key):
        self.cache_key = f"{CACHE_KEY_TEMPLATE.get('upload_part_info_key')}_{locker_key}"
        super().__init__(self.cache_key)


class DownloadUrlCache(RedisCacheBase):
    def __init__(self, drive_id, file_id):
        self.cache_key = f"{CACHE_KEY_TEMPLATE.get('download_url_key')}_{drive_id}_{file_id}"
        super().__init__(self.cache_key)


class DriveQrCache(RedisCacheBase):
    def __init__(self, locker_key):
        self.cache_key = f"{CACHE_KEY_TEMPLATE.get('drive_qrcode_key')}_{locker_key}"
        super().__init__(self.cache_key)


class GradingClickCache(RedisCacheBase):
    def __init__(self, book_id, client_id):
        self.cache_key = f"{CACHE_KEY_TEMPLATE.get('book_grading_click_key')}_{client_id}_{book_id}"
        super().__init__(self.cache_key, timeout=24 * 3600)


class BookDownloadCache(RedisCacheBase):
    def __init__(self, book_id):
        self.cache_key = f"{CACHE_KEY_TEMPLATE.get('book_download_increase_key')}_{book_id}"
        super().__init__(self.cache_key, timeout=24 * 3600)


class BookGradingCache(RedisCacheBase):
    def __init__(self, book_id):
        self.cache_key = f"{CACHE_KEY_TEMPLATE.get('book_grading_increase_key')}_{book_id}"
        super().__init__(self.cache_key, timeout=24 * 3600)
