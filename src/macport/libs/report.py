from __future__ import annotations

from ..collecter import (
    GithubEndpointCollect,
    DjangoEndPointCollect
)


class Report:
    def __init__(self, github_endpoint_collect: GithubEndpointCollect,
                 django_endpoint_collect: DjangoEndPointCollect):
        self.github_endpoint_collect = github_endpoint_collect
        self.develop_endpoint_collect = django_endpoint_collect

    def todo_document(self):
        """ 개발된 문서에만 존재하는 API """

        return {
            '/api/admin': set(self.develop_endpoint_collect.result['/api/admin']) - set(
                self.github_endpoint_collect.result['/api/admin']),

            '/api/user': set(self.develop_endpoint_collect.result['/api/user']) - set(
                self.github_endpoint_collect.result['/api/user'])
        }

    def summary(self):
        return {
            'count': {
                'total': len(self.develop_endpoint_collect.endpoints),
                'detail': {
                    'api/admin': len(
                        [item for item in self.develop_endpoint_collect.endpoints if item.prefix == 'api/admin/']),
                    'api/user': len(
                        [item for item in self.develop_endpoint_collect.endpoints if item.prefix == 'api/user/']),
                    'api/operation': len(
                        [item for item in self.develop_endpoint_collect.endpoints if item.prefix == 'api/operation/'])
                },
                'test': {
                    'need': len(
                        [item for item in self.develop_endpoint_collect.endpoints if item.name is None]),
                    'complete': len(
                        [item for item in self.develop_endpoint_collect.endpoints if item.name is not None])
                }
            }
