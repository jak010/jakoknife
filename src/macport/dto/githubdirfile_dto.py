from dataclasses import dataclass


@dataclass
class GithubDirFileDto:
    name: str
    path: str
    sha: str
    size: int
    url: str
    html_url: str
    git_url: str
    download_url: str
    type: str
    _links: dict
