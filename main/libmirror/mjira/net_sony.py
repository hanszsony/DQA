__API_VERSION = 1

from urllib.parse import quote
from jira import JIRA

import mconfig
from mjira.const import API, HOST_SONY
import mjira.http
from mlogger import LOGGER


# ------------------------ Headers ---------------------------


def __get_sony_headers():
    token = mconfig.get_sony_jira_token()
    return {
        "Content-Type": "application/json",
        "User-Agent": "JIRA",
        "Authorization": f"Bearer {token}",
    }


# ------------------------ Get ---------------------------


def get_sony_jira(key: str):
    """Fetch the details of a Sony Jira issue by its key.

    :param key: The key of the Jira issue to retrieve.
    :return: JSON object containing issue details.
    """
    return mjira.http.get(__get_sony_headers(), API.SONY_ISSUE.format(key))


# ------------------------ Search ---------------------------


def search_sony_jira(filter: str):
    """Search for Sony Jira issues.

    :param filter: The JQL filter string to search for issues.
    :return: JSON object containing the search results.
    """
    return mjira.http.get(
        __get_sony_headers(),
        API.SONY_SEARCH.format(quote(filter)),
    )


SPLIT_LEN = 50


def search_sony_jira_in_params(filter: str, field_list: list, max_results: int = -1):
    """Search for Sony Jira issues with specific fields.

    :param filter: The JQL filter string to search for issues.
    :param field_list: A list of fields to include in the results.
    :param max_results: Maximum number of results to return; -1 for no limit.
    :return: JSON object containing the search results.
    """

    fields = ",".join(field_list)
    url = API.SONY_SEARCH_PARMAS.format(
        jql=quote(filter), fields=fields, max_results=max_results
    )
    return mjira.http.get(__get_sony_headers(), url)


def search_sony_jira_expand_changelog_split(filter: str, split_seq: int):
    """Search for Sony Jira issues with changelog and pagination support.

    :param filter: The JQL filter string to search for issues.
    :param split_seq: The page number to retrieve, used for pagination.
    :return: JSON object containing the search results with changelog.
    """
    return mjira.http.get(
        __get_sony_headers(),
        API.SONY_SEARCH_CHANGELOG_SPLITED.format(
            jql=quote(filter), start_at=split_seq * SPLIT_LEN, max_results=SPLIT_LEN
        ),
    )


# ------------------------ Download ---------------------------


def download_sony_attachment(
    url: str,
    file_name: str,
    file_folder: str,
):
    """
    Download attachment from sony jira center
    :param url: The URL of the image
    :param file_path_all: The local file path to save the image
    """
    import os
    import requests

    LOGGER.debug(f"[download_sony_attachment] Start download img from: {url}")
    try:
        headers = __get_sony_headers()
        # Ensure the directory exists
        if not os.path.exists(file_folder):
            os.makedirs(file_folder, exist_ok=True)
            LOGGER.debug(f"Target folder created: {file_folder}")

        # Download the image
        response = requests.get(url, stream=True, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        with open(os.path.join(file_folder, file_name), "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        LOGGER.debug(f"Image successfully downloaded: {file_name}")
    except requests.RequestException as req_err:
        LOGGER.error(f"Network error downloading image: {req_err}")
    except IOError as io_err:
        LOGGER.error(f"File I/O error: {io_err}")
    except Exception as e:
        LOGGER.error(f"Unexpected error downloading image: {e}")


# -------------------------- Jira ----------------------------

def update_sony_jira(key: str, data_issue: dict):
    """Update an existing Sony Jira issue.

    :param key: The key of the Jira issue to update.
    :param data_issue: A dictionary containing the fields to update.
    :return: None
    """
    LOGGER.debug(f"updating Sony jira {key} with data: {data_issue}")
    update_result = False
    try:
        jira_conn = JIRA(
            server=HOST_SONY,
            token_auth=mconfig.get_sony_jira_token(),
        )
        issue = jira_conn.issue(key)
        issue.update(fields=data_issue)
        LOGGER.info("Issue updated successfully!")
        update_result = True
        return update_result
    except Exception as e:
        update_result = False
        LOGGER.error("Exception: " + str(e))


def transition_sony_jira_fields(key: str, new_status: str, fields: dict):
    """Transition a Sony Jira issue to a new status with additional fields.

    :param key: The key of the Jira issue to transition.
    :param new_status: The new status to which the issue should be transitioned.
    :param fields: A dictionary of additional fields to update during the transition.
    :return: None
    """
    LOGGER.debug(
        f"transitioning Sony jira {key} to status {new_status} with fields: {fields}"
    )
    try:
        jira_conn = JIRA(
            server=HOST_SONY,
            token_auth=mconfig.get_sony_jira_token(),
        )
        issue = jira_conn.issue(key)
        jira_conn.transition_issue(issue, transition=new_status, fields=fields)
        LOGGER.info("Issue transited successfully!")
    except Exception as e:
        LOGGER.error("Exception: " + str(e))
