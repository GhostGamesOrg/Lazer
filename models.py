from typing import Dict, Any


class Error:
    def __init__(self, status: int, reason: str):
        self.status: int = status
        self.reason: str = reason

    def serialize(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "reason": self.reason,
        }


class User:
    def __init__(self, id: int, name: str, avatar: str, description: str, github_url: str):
        self.id: int = id
        self.name: str = name
        self.avatar: str = avatar
        self.description: str = description
        self.github_url: str = github_url

    def serialize(self) -> Dict[str, Any]:
        return {
            "id":           self.id,
            "name":         self.name,
            "avatar":       self.avatar,
            "description":  self.description,
            "github_url":   self.github_url,
        }


class Package:
    def __init__(self, name: str, author_id: int, github_url: str, avatar: str):
        self.name: str = name
        self.author_id: int = author_id
        self.github_url: str = github_url
        self.avatar: str = avatar

    def serialize(self) -> Dict[str, Any]:
        return {
            "name":         self.name,
            "author_id":    self.author_id,
            "github_url":   self.github_url,
            "avatar":       self.avatar,
        }


class Release:
    def __init__(self, package_name: str, contributor_id: int, description: str, version: str, date: int, downloads: int):
        self.package_name: str = package_name
        self.contributor_id: int = contributor_id
        self.description: str = description
        self.version: str = version
        self.date: int = date
        self.downloads: int = downloads

    def serialize(self) -> Dict[str, Any]:
        return {
            "package_name": self.package_name,
            "contributor_id": self.contributor_id,
            "description": self.description,
            "version": self.version,
            "date": self.date,
            "downloads": self.downloads
        }
