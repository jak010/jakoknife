from __future__ import annotations

import os
import re
from functools import cached_property
from typing import List

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django

django.setup()

from django.urls import URLResolver
from django.urls.resolvers import RegexPattern
from django.conf import settings


class EndPointMeta:
    def __init__(self, prefix, pattern, name):
        self.prefix = prefix  # Ex, api/user/ or api/admin/
        self.pattern = pattern
        self.name = None if name == 'None' else name

    def __repr__(self):
        return f"[Prefix=]{self.prefix},\n" \
               f"[Pattern=]{self.pattern},\n" \
               f"[Name=]{self.name}"


class DjangoEndPointCollect:
    ROOT_URL_CONF = settings.ROOT_URLCONF

    def __init__(self):
        self.endpoints: List[EndPointMeta] = []
        self._result = self._execute()

    @cached_property
    def root(self) -> URLResolver:
        return URLResolver(RegexPattern(r"^/"), self.ROOT_URL_CONF)

    def all_endpoint(self):
        return self.endpoints

    @cached_property
    def result(self):
        return self._result

    def _execute(self):
        result = {'/api/admin': [], '/api/user': []}
        root_patterns: List[URLResolver] = [root_url_pattern for root_url_pattern in self.root.url_patterns]
        for root_pattern in root_patterns:
            for sub_pattern in root_pattern.url_patterns:
                endpoint = EndPointMeta(prefix=str(root_pattern.pattern),
                                        pattern=str(sub_pattern.pattern),
                                        name=str(sub_pattern.name))
                self.endpoints.append(endpoint)

                # 개발이 완료된 EndPoint는 정규표현식을 사용하기 때문에 StopLight랑 Endpoint 표현방식이 다름
                regex = r'<[^:>]+:(?P<name>[a-zA-Z0-9_\-]+)>'
                lookup = re.findall(regex, endpoint.pattern)
                if lookup:
                    for replace_str in lookup:
                        endpoint.pattern = re.sub(regex, "{" + replace_str + "}", endpoint.pattern)

                self._admin_collect(result, endpoint.prefix, endpoint.pattern)
                self._user_collect(result, endpoint.prefix, endpoint.pattern)

        return result

    def _user_collect(self, result, root_pattern, sub_pattern):
        if self._is_user(domain=root_pattern):
            result['/api/user'].append("/" + sub_pattern)

    def _admin_collect(self, result, root_pattern, sub_pattern):
        if self._is_admin(domain=root_pattern):
            result['/api/admin'].append("/" + sub_pattern)

    def _is_admin(self, domain):
        return domain == 'api/admin/'

    def _is_user(self, domain):
        return domain == 'api/user/'
