import re
import requests
import os.path

NAME = "github"
TYPE = ["poll", "hook"]
API_VERSION = 1


class Poll(object):
    def __init__(self, url, extra_data=None):
        if extra_data["watch"] != "tags":
            raise NotImplementedError("Only watching for new tags is supported right now.")
        # TODO: Support watching heads

        self._url = url
        self._tag_regex = re.compile(extra_data["tag"])

    def _get_repo(self):
        url_sans_extension = os.path.splitext(self._url)[0]
        url_parts = url_sans_extension.split("/")
        return url_parts[3:5]

    def _parse_api_tags(self, response_json):
        tags = []
        for node in response_json:
            tag_match = self._tag_regex.fullmatch(node["ref"])
            if tag_match:
                tags.append(tag_match.groups())

        return tags

    def get_version(self):
        parts = self._get_repo()
        if len(parts) < 2:
            raise ValueError("Invalid URL")

        # Query Github API
        query_url = "https://api.github.com/repos/{0}/{1}/git/refs/tags".format(*parts)
        response = requests.get(query_url)
        if response.status_code != 200:
            raise RuntimeError("Repository '{1}' by '{0}' not found.".format(*parts))

        # Get API tags
        tags = self._parse_api_tags(response.json())

        # Get latest tag
        latest_tag = tags[0]
        for tag in tags:
            if tag[1] > latest_tag[1]:
                latest_tag = tag

        return latest_tag


class Hook(object):
    def __init__(self, url, extra_data=None):
        print("{0} hook init successful.".format(NAME))

    def success(self):
        print("{0} hooking import success!".format(NAME))
