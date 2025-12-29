__API_VERSION = 1

from typing import List
import json
import base64
import requests

import mconfig
from mlogger import LOGGER

ZT_URL = mconfig.get_host_zt()
ZT_HTTP_BASIC = mconfig.get_zt_http_basic()
ZT_USERNAME = mconfig.get_zt_username()
ZT_PASSWORD = mconfig.get_zt_password()

cookies = {}
login_data = f"account={ZT_USERNAME}&password={ZT_PASSWORD}"


def __get_text_header():
    base64_auth = base64.b64encode(ZT_HTTP_BASIC.encode("utf-8")).decode("utf-8")
    return {
        "Authorization": f"Basic {base64_auth}",
        "Accept": "application/json; charset=UTF-8",
        "Content-Type": "text/html; Language=UTF-8; charset=UTF-8",
    }


def __get_forms_header():
    base64_auth = base64.b64encode(ZT_HTTP_BASIC.encode("utf-8")).decode("utf-8")
    return {
        "Referer": ZT_URL,
        "Authorization": f"Basic {base64_auth}",
        "Content-Type": "application/x-www-form-urlencoded",
    }


def __get_raw_header():
    base64_auth = base64.b64encode(ZT_HTTP_BASIC.encode("utf-8")).decode("utf-8")
    # 这个为啥有bug id?
    return {
        # "Referer": ZT_URL + "/index.php?m=bug&f=edit&bugID=2685",
        "Referer": ZT_URL + "/index.php",
        "Authorization": f"Basic {base64_auth}",
        # "Content-Type": "multipart/form-data",
    }


def __get(headers, url):
    LOGGER.debug(f"GET data from: {url}")
    global cookies
    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        LOGGER.debug("succeed to GET")
        try:
            response_json = response.json()
            return response_json
        except ValueError:
            LOGGER.debug("Response is not JSON format")
            LOGGER.debug(response.content)
    else:
        LOGGER.error(
            f"failed to GET : {response.status_code}\nreponse message: {response.content}"
        )


def __post(headers, url, data, files=None):
    LOGGER.debug(f"POST api data to: {url}")
    global cookies
    response = requests.post(
        url, headers=headers, cookies=cookies, data=data, files=files
    )
    if response.status_code == 200:
        LOGGER.debug("succeed to POST")
        response_json = None
        respone_html = response.content
        try:
            response_json = response.json()
        except ValueError:
            LOGGER.debug("Response is not JSON format")
        return response_json, respone_html
    else:
        LOGGER.error(
            f"failed to POST : {response.status_code}\nreponse message: {response.content}"
        )


# ------------------------------------------ Login Auth ---------------------------------------------


def __set_up_cookies() -> dict:
    """
    Sample for returing msg:
    {
        'status': 'success',
        'data': '{"title":"","sessionName":"zentaosid","sessionID":"...","rand":5730,"pager":null}',
        'md5': '...'
    }
    """
    url = f"{ZT_URL}?m=api&f=getSessionID&t=json"
    headers = __get_text_header()
    response_json = __get(headers, url)
    session_data = json.loads(response_json["data"])
    session_name = session_data["sessionName"]
    session_id = session_data["sessionID"]
    global cookies
    cookies[session_name] = session_id


def __login():
    __set_up_cookies()
    url = f"{ZT_URL}?m=user&f=login&t=json"
    global login_data
    headers = __get_forms_header()
    result_json, result_html = __post(headers, url, login_data)
    login_status = result_json["status"] == "success" if result_json else False
    assert login_status, "Login Failure!"


# ------------------------------------------ HTTP Public of Read ---------------------------------------------


def get_bug_list(product_id: int, bug_status: str):
    __login()
    url = f"{ZT_URL}?m=bug&f=browse&productID={product_id}&branch=0&browseType={bug_status}&param=0&orderBy=&recTotal=999999&recPerPage=999999&t=json"
    headers = __get_text_header()
    return __get(headers, url)


# ------------------------------------------ HTTP Public of Write ---------------------------------------------


def __get_formatted_files(asset_path_all_list: List[str]):
    import os
    import mimetypes

    files = []
    for asset_path_all in asset_path_all_list:
        asset_name = os.path.basename(asset_path_all)
        mime_type, _ = mimetypes.guess_type(asset_path_all)
        LOGGER.debug(f"Upload {asset_name} with mime type {mime_type}.")
        files.append(
            (
                "files[]",
                (
                    asset_name,
                    open(asset_path_all, "rb"),
                    mime_type,
                ),
            )
        )
    print(files)
    return files


def __get_zt_id_from_html(html):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "lxml")
    id_span = soup.find("span", class_="label label-id")
    zt_id = id_span.text
    return zt_id


def __get_zt_id_from_added_json(added_info_json):
    added_info_data = json.loads(added_info_json["data"])
    added_zt_id = added_info_data["bugs"][0]["id"]
    return added_zt_id


# 返回Json示例：
# {
#    'result': 'success',
#    'message': '保存成功',
#    'locate': '/index.php?m=bug&f=browse&t=json&productID=39&branch=&browseType=unclosed&param=0&orderBy=id_desc'
# }


def add_bug(bug_params: dict, asset_path_all_list: List[str] = None):
    __login()
    product_id = bug_params["product"]
    url = f"{ZT_URL}?m=bug&f=create&productID={product_id}&t=json"  # PHP API
    # url = f"{ZT_URL}/index.php?m=bug&f=create&productID={product_id}&branch=0&extra=moduleID=0" # HTTP
    headers = __get_raw_header()
    if asset_path_all_list:
        files = __get_formatted_files(asset_path_all_list)
        result_json, _ = __post(headers, url, bug_params, files)
    else:
        result_json, _ = __post(headers, url, bug_params)
    added_info_json_url = ZT_URL + "/" + result_json["locate"]
    added_info_json = __get(headers, added_info_json_url)
    added_zt_id = __get_zt_id_from_added_json(added_info_json)
    return ((result_json["result"] == "success") if result_json else False), added_zt_id


def update_bug(bug_id: int, bug_params: dict, asset_path_all_list: List[str] = None):
    __login()
    url = f"{ZT_URL}/index.php?m=bug&f=edit&bugID={bug_id}"
    headers = __get_raw_header()
    if asset_path_all_list:
        files = __get_formatted_files(asset_path_all_list)
        result_json, result_html = __post(headers, url, bug_params, files)
    else:
        result_json, result_html = __post(headers, url, bug_params)
    return (
        (result_json["status"] == 1) if result_json else True  # 不清楚怎么确认是否成功
    ), __get_zt_id_from_html(result_html)
