import re

import pyshorteners


def is_true(env_variable):
    return env_variable.lower() in ("true", "1", "t")


def remove_slack_mentions(text: str) -> str:
    return re.sub("<@.*>", "", text)


def encode_url(url: str) -> str:
    print(f"{url=}")
    encoded_url = url.replace("{", "%7B").replace("}", "%7D").replace(" ", "%20")
    print(f"{encoded_url=}")
    return encoded_url


def shorten_url(long_url: str) -> str:
    print(f"{long_url=}")
    type_tiny = pyshorteners.Shortener()
    short_url = type_tiny.tinyurl.short(long_url)
    print(f"{short_url=}")
    return short_url
