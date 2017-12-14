import json

import hashlib

from django.utils import encoding
from django.conf import settings as djangosettings
from django.core.cache import cache

notcachedRemoteAddress = ['188.184.185.129']

def deleteCacheTestData(request,data):
### Filtering data
    if request.user.is_authenticated() and request.user.is_tester:
        return data
    else:
        if data is not None:
            for key in data.keys():
                if '_test' in key:
                    del data[key]
    return data

def getCacheEntry(request, viewType, skipCentralRefresh = False, isData = False):
    is_json = False

    # We do this check to always rebuild cache for the page when it called from the crawler
    if (('HTTP_X_FORWARDED_FOR' in request.META) and (request.META['HTTP_X_FORWARDED_FOR'] in notcachedRemoteAddress) and
                skipCentralRefresh == False):
        return None

    request._cache_update_cache = False
    if ((('HTTP_ACCEPT' in request.META) and (request.META.get('HTTP_ACCEPT') in ('application/json'))) or (
                'json' in request.GET)):
        is_json = True
    key_prefix = "%s_%s_%s_" % (is_json, djangosettings.CACHE_MIDDLEWARE_KEY_PREFIX, viewType)
    if isData==False:
        try:
            if request.method == "POST":
                path = hashlib.md5(encoding.force_bytes(encoding.iri_to_uri(request.get_full_path() + '?' + request.body)))
            else:
                path = hashlib.md5(encoding.force_bytes(encoding.iri_to_uri(request.get_full_path())))
        except: path = hashlib.md5(encoding.force_bytes(encoding.iri_to_uri(request.get_full_path())))
        cache_key = '%s.%s' % (key_prefix, path.hexdigest())
        return cache.get(cache_key, None)
    else:
        cache_key = '%s' % (key_prefix)
        return cache.get(cache_key, None)


def setCacheEntry(request, viewType, data, timeout, isData = False):
    is_json = False
    request._cache_update_cache = False
    if ((('HTTP_ACCEPT' in request.META) and (request.META.get('HTTP_ACCEPT') in ('application/json'))) or (
                'json' in request.GET)):
        is_json = True
    key_prefix = "%s_%s_%s_" % (is_json, djangosettings.CACHE_MIDDLEWARE_KEY_PREFIX, viewType)
    if isData==False:
        try:
            if request.method == "POST":
                path = hashlib.md5(encoding.force_bytes(encoding.iri_to_uri(request.get_full_path() + '?' + request.body)))
            else:
                path = hashlib.md5(encoding.force_bytes(encoding.iri_to_uri(request.get_full_path())))
        except: path = hashlib.md5(encoding.force_bytes(encoding.iri_to_uri(request.get_full_path())))
        cache_key = '%s.%s' % (key_prefix, path.hexdigest())
    else:
        cache_key = '%s' % (key_prefix)
    cache.set(cache_key, data, timeout)