from __future__ import annotations

import base64
import json
from typing import List

import requests

from ..dto.githubdirfile_dto import GithubDirFileDto


class GithubApi:

    def __init__(self):
        self.base_url = "https://api.github.com/repos/tesnine/"
        self.token = ''
        self.headers = {
            'Authorization': 'Bearer ' + self.token,
            'Accept': 'application/vnd.github+json',
            "X-GitHub-Api-Version": "2022-11-28"
        }

    def get_listdir(self, repository_name, dir_name) -> List[GithubDirFileDto]:
        r = requests.get(
            url=f"https://api.github.com/repos/tesnine/{repository_name}/contents/{dir_name}",
            headers=self.headers
        )
        if r.status_code == 200:
            return [GithubDirFileDto(**item) for item in r.json()]
        raise Exception(f"Request Failure... {self.__class__.__name__}")

    def get_file_content(self, repository_name, file_sha):
        r = requests.get(
            url=f"https://api.github.com/repos/tesnine/{repository_name}/git/blobs/{file_sha}",
            headers=self.headers
        )
        if r.status_code == 200:
            content = r.json()['content']
            return json.loads(base64.b64decode(content).decode())
