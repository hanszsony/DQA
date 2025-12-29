__API_VERSION = 1

from mlogger import LOGGER

from urllib.request import Request, HTTPError
from urllib.request import urlopen
from json import loads, dumps


ENCODE = "UTF-8"


def get(headers: dict, url: str):
    try:
        LOGGER.debug(f"get url:{url}")
        request = Request(url=url, method="GET", headers=headers)
        response = urlopen(request)
        response_body = response.read().decode(ENCODE)
        return loads(response_body)
    except HTTPError as e:
        LOGGER.warning(f"HTTP Error {e.code}: {e.reason}")
        LOGGER.error(e.read().decode(ENCODE))


def put(headers: dict, url: str, data):
    try:
        LOGGER.debug(f"put url:{url}")
        request = Request(
            url=url, method="PUT", headers=headers, data=dumps(data).encode(ENCODE)
        )
        response = urlopen(request)
        response_body = response.read().decode(ENCODE)
        return response_body
    except HTTPError as e:
        LOGGER.warning(f"HTTP Error {e.code}: {e.reason}")
        LOGGER.error(e.read().decode(ENCODE))


def post(headers: dict, url: str, data):
    try:
        LOGGER.debug(f"post url:{url}")
        request = Request(
            url, method="POST", headers=headers, data=dumps(data).encode(ENCODE)
        )
        response = urlopen(request)
        response_body = response.read().decode(ENCODE)
        return loads(response_body)
    except HTTPError as e:
        LOGGER.warning(f"HTTP Error {e.code}: {e.reason}")
        LOGGER.error(e.read().decode(ENCODE))


def delete(headers: dict, url: str):
    try:
        LOGGER.debug(f"delete url: {url}")
        request = Request(url, method="DELETE", headers=headers)
        response = urlopen(request)

        if response.status == 204:
            LOGGER.info(f"Resource deleted successfully at {url}")
            return True
        else:
            LOGGER.warning(f"Unexpected response status: {response.status}")
            return False
    except HTTPError as e:
        LOGGER.warning(f"HTTP Error {e.code}: {e.reason}")
        LOGGER.error(e.read())
        return False
