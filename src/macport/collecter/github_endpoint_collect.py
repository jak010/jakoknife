from __future__ import annotations

from functools import cached_property
from ..gh_client.client import GithubApi


class GithubEndpointCollect:
    def __init__(self):
        self.github_client = GithubApi()
        self._repositories = ["mac-admin-document", "mac-user-document"]

        self._result = self._execute()

    @cached_property
    def result(self):
        return self._result

    def _execute(self):
        result = {'/api/admin': [], '/api/user': []}
        for repo in self._repositories:
            for f in self.github_client.get_listdir(repository_name=repo, dir_name='reference'):
                file_content = self.get_content(f, repo)

                domain = self.api_root(file_content)
                self._admin_collect(domain, file_content, result)
                self._user_collect(domain, file_content, result)

        return result

    def api_root(self, file_content):
        return '/'.join(file_content['servers'][0]['url'].split("/")[-2::])

    def get_content(self, f, repo):
        return self.github_client.get_file_content(repository_name=repo, file_sha=f.sha)

    def _user_collect(self, domain, file_content, result):
        if self._is_user(domain):
            for path in file_content['paths'].keys():
                result['/api/user'].append(path)

    def _admin_collect(self, domain, file_content, result):
        if self._is_admin(domain):
            for path in file_content['paths'].keys():
                result['/api/admin'].append(path)

    def _is_admin(self, domain):
        return domain == 'api/admin'

    def _is_user(self, domain):
        return domain == 'api/user'
