__API_VERSION = 1

from mlogger import LOGGER

from mio import get_json_from_file

try:
    __CONFIG_JSON = get_json_from_file(".config")
except Exception as e:
    LOGGER.error(f"读取配置文件失败: {e}")

__CONFIG_KEY_ISSUE_LIST_FILE_PATH = "issue_list_file_path"
__CONFIG_VALUE_ISSUE_LIST_FILE_PATH = None

def get_issue_list_file_path() -> str:
    global __CONFIG_VALUE_ISSUE_LIST_FILE_PATH
    if __CONFIG_VALUE_ISSUE_LIST_FILE_PATH == None:
        if __CONFIG_KEY_ISSUE_LIST_FILE_PATH not in __CONFIG_JSON:
            LOGGER.error(f'请补充配置"{__CONFIG_KEY_ISSUE_LIST_FILE_PATH}"到.config\n')
        __CONFIG_VALUE_ISSUE_LIST_FILE_PATH = __CONFIG_JSON[__CONFIG_KEY_ISSUE_LIST_FILE_PATH]
    return __CONFIG_VALUE_ISSUE_LIST_FILE_PATH
    
__CONFIG_KEY_SONY_JIRA_TOKEN = "sony_jira_token"
__CONFIG_VALUE_SONY_JIRA_TOKEN = None

def get_sony_jira_token() -> str:
    global __CONFIG_VALUE_SONY_JIRA_TOKEN
    if __CONFIG_VALUE_SONY_JIRA_TOKEN == None:
        if __CONFIG_KEY_SONY_JIRA_TOKEN not in __CONFIG_JSON:
            LOGGER.error(f'请补充配置"{__CONFIG_KEY_SONY_JIRA_TOKEN}"到.config\n')
        __CONFIG_VALUE_SONY_JIRA_TOKEN = __CONFIG_JSON[__CONFIG_KEY_SONY_JIRA_TOKEN]
    return __CONFIG_VALUE_SONY_JIRA_TOKEN


__CONFIG_KEY_ZT_URL = "zt_url"
__CONFIG_VALUE_ZT_URL = None

def get_zt_url() -> str:
    global __CONFIG_VALUE_ZT_URL
    if __CONFIG_VALUE_ZT_URL == None:
        if __CONFIG_KEY_ZT_URL not in __CONFIG_JSON:
            LOGGER.error(f'请补充配置"{__CONFIG_KEY_ZT_URL}"到.config\n')
        __CONFIG_VALUE_ZT_URL = __CONFIG_JSON[__CONFIG_KEY_ZT_URL]
    return __CONFIG_VALUE_ZT_URL


__CONFIG_KEY_ZT_HTTP_BASIC = "zt_http_basic"
__CONFIG_VALUE_ZT_HTTP_BASIC = None

def get_zt_http_basic() -> str:
    global __CONFIG_VALUE_ZT_HTTP_BASIC
    if __CONFIG_VALUE_ZT_HTTP_BASIC == None:
        if __CONFIG_KEY_ZT_HTTP_BASIC not in __CONFIG_JSON:
            LOGGER.error(f'请补充配置"{__CONFIG_KEY_ZT_HTTP_BASIC}"到.config\n')
        __CONFIG_VALUE_ZT_HTTP_BASIC = __CONFIG_JSON[__CONFIG_KEY_ZT_HTTP_BASIC]
    return __CONFIG_VALUE_ZT_HTTP_BASIC


__CONFIG_KEY_ZT_USERNAME = "zt_username"
__CONFIG_VALUE_ZT_USERNAME = None

def get_zt_username() -> str:
    global __CONFIG_VALUE_ZT_USERNAME
    if __CONFIG_VALUE_ZT_USERNAME == None:
        if __CONFIG_KEY_ZT_USERNAME not in __CONFIG_JSON:
            LOGGER.error(f'请补充配置"{__CONFIG_KEY_ZT_USERNAME}"到.config\n')
        __CONFIG_VALUE_ZT_USERNAME = __CONFIG_JSON[__CONFIG_KEY_ZT_USERNAME]
    return __CONFIG_VALUE_ZT_USERNAME


__CONFIG_KEY_ZT_PASSWORD = "zt_password"
__CONFIG_VALUE_ZT_PASSWORD = None

def get_zt_password() -> str:
    global __CONFIG_VALUE_ZT_PASSWORD
    if __CONFIG_VALUE_ZT_PASSWORD == None:
        if __CONFIG_KEY_ZT_PASSWORD not in __CONFIG_JSON:
            LOGGER.error(f'请补充配置"{__CONFIG_KEY_ZT_PASSWORD}"到.config\n')
        __CONFIG_VALUE_ZT_PASSWORD = __CONFIG_JSON[__CONFIG_KEY_ZT_PASSWORD]
    return __CONFIG_VALUE_ZT_PASSWORD


__CONFIG_KEY_ZT_URL = "host_zt"
__CONFIG_VALUE_ZT_URL = None


def get_host_zt() -> str:
    global __CONFIG_VALUE_ZT_URL
    if __CONFIG_VALUE_ZT_URL == None:
        if __CONFIG_KEY_ZT_URL not in __CONFIG_JSON:
            LOGGER.error(f'请补充配置"{__CONFIG_KEY_ZT_URL}"到.config\n')
        __CONFIG_VALUE_ZT_URL = __CONFIG_JSON[__CONFIG_KEY_ZT_URL]
    return __CONFIG_VALUE_ZT_URL


__CONFIG_KEY_DB_MANAGER = "db_manager"
__CONFIG_VALUE_DB_MANAGER = None


def get_db_manager() -> str:
    global __CONFIG_VALUE_DB_MANAGER
    if __CONFIG_VALUE_DB_MANAGER == None:
        if __CONFIG_KEY_DB_MANAGER not in __CONFIG_JSON:
            LOGGER.error(f'请补充配置"{__CONFIG_KEY_DB_MANAGER}"到.config\n')
        __CONFIG_VALUE_DB_MANAGER = __CONFIG_JSON[__CONFIG_KEY_DB_MANAGER]
    return __CONFIG_VALUE_DB_MANAGER


__CONFIG_KEY_TO_ZT_BUG_SECTION_PARENT = "to_zt_bug_section"
__CONFIG_KEY_TO_ZT_BUG_SECTION_PICKED = "picked"
__CONFIG_VALUE_TO_BUG_SECTION = None


def get_to_zt_bug_section() -> str:
    global __CONFIG_VALUE_TO_BUG_SECTION
    #if __CONFIG_VALUE_TO_BUG_SECTION == None:
    #    if __CONFIG_KEY_TO_ZT_BUG_SECTION_PARENT not in __CONFIG_JSON:
    #        LOGGER.error(
    #            f'请补充配置"{__CONFIG_KEY_TO_ZT_BUG_SECTION_PARENT}"到.config'
    #        )
    #    if (
    #        __CONFIG_KEY_TO_ZT_BUG_SECTION_PICKED
    #        not in __CONFIG_JSON[__CONFIG_KEY_TO_ZT_BUG_SECTION_PARENT]
    #    ):
    #        LOGGER.error(
    #            f'请补充配置"{__CONFIG_KEY_TO_ZT_BUG_SECTION_PICKED}"到.config'
    #        )
    #    __CONFIG_VALUE_TO_BUG_SECTION = __CONFIG_JSON[
    #        __CONFIG_KEY_TO_ZT_BUG_SECTION_PARENT
    #    ][__CONFIG_KEY_TO_ZT_BUG_SECTION_PICKED]
    return __CONFIG_VALUE_TO_BUG_SECTION


__CONFIG_KEY_TRANS_ARTIFACTS = "trans_artifacts"
__CONFIG_VALUE_TRANS_ARTIFACTS = None


def get_trans_artifacts() -> bool:
    global __CONFIG_VALUE_TRANS_ARTIFACTS
    if __CONFIG_VALUE_TRANS_ARTIFACTS == None:
        if __CONFIG_KEY_TRANS_ARTIFACTS not in __CONFIG_JSON:
            LOGGER.error(f'请补充配置"{__CONFIG_KEY_TRANS_ARTIFACTS}"到.config')
        __CONFIG_VALUE_TRANS_ARTIFACTS = __CONFIG_JSON[__CONFIG_KEY_TRANS_ARTIFACTS]
    return __CONFIG_VALUE_TRANS_ARTIFACTS


__CONFIG_KEY_TRANS_DESCRIPTIONS = "trans_descriptions"
__CONFIG_VALUE_TRANS_DESCRIPTIONS = None


def get_trans_descriptions() -> bool:
    global __CONFIG_VALUE_TRANS_DESCRIPTIONS
    if __CONFIG_VALUE_TRANS_DESCRIPTIONS == None:
        if __CONFIG_KEY_TRANS_DESCRIPTIONS not in __CONFIG_JSON:
            LOGGER.error(f'请补充配置"{__CONFIG_KEY_TRANS_DESCRIPTIONS}"到.config\n')
        __CONFIG_VALUE_TRANS_DESCRIPTIONS = __CONFIG_JSON[
            __CONFIG_KEY_TRANS_DESCRIPTIONS
        ]
    return __CONFIG_VALUE_TRANS_DESCRIPTIONS


__CONFIG_KEY_HOST_SONY = "host_sony"
__CONFIG_VALUE_HOST_SONY = None


def get_host_sony() -> bool:
    global __CONFIG_VALUE_HOST_SONY
    if __CONFIG_VALUE_HOST_SONY == None:
        if __CONFIG_KEY_HOST_SONY not in __CONFIG_JSON:
            LOGGER.error(f'请补充配置"{__CONFIG_KEY_HOST_SONY}"到.config\n')
        __CONFIG_VALUE_HOST_SONY = __CONFIG_JSON[__CONFIG_KEY_HOST_SONY]
    return __CONFIG_VALUE_HOST_SONY


__CONFIG_KEY_HOST_CSC = "host_csc"
__CONFIG_VALUE_HOST_CSC = None


__CONFIG_KEY_HOST_TAPD = "host_tapd"
__CONFIG_VALUE_HOST_TAPD = None


def get_host_tapd() -> bool:
    global __CONFIG_VALUE_HOST_TAPD
    if __CONFIG_VALUE_HOST_TAPD == None:
        if __CONFIG_KEY_HOST_TAPD not in __CONFIG_JSON:
            LOGGER.error(f'请补充配置"{__CONFIG_KEY_HOST_TAPD}"到.config\n')
        __CONFIG_VALUE_HOST_TAPD = __CONFIG_JSON[__CONFIG_KEY_HOST_TAPD]
    return __CONFIG_VALUE_HOST_TAPD


__CONFIG_KEY_GERRIT_SUBMIT_REPO = "gerrit_submit_repo"
__CONFIG_VALUE_GERRIT_SUBMIT_REPO = None


def get_gerrit_submit_repo() -> bool:
    global __CONFIG_VALUE_GERRIT_SUBMIT_REPO
    if __CONFIG_VALUE_GERRIT_SUBMIT_REPO == None:
        if __CONFIG_KEY_GERRIT_SUBMIT_REPO not in __CONFIG_JSON:
            LOGGER.error(f'请补充配置"{__CONFIG_KEY_GERRIT_SUBMIT_REPO}"到.config\n')
        __CONFIG_VALUE_GERRIT_SUBMIT_REPO = __CONFIG_JSON[
            __CONFIG_KEY_GERRIT_SUBMIT_REPO
        ]
    return __CONFIG_VALUE_GERRIT_SUBMIT_REPO


__CONFIG_KEY_GERRIT_SUBMIT_REPO_T6Y = "gerrit_submit_repo_t6y"
__CONFIG_VALUE_GERRIT_SUBMIT_REPO_T6Y = None


def get_gerrit_submit_repo_t6y() -> bool:
    global __CONFIG_VALUE_GERRIT_SUBMIT_REPO_T6Y
    if __CONFIG_VALUE_GERRIT_SUBMIT_REPO_T6Y == None:
        if __CONFIG_KEY_GERRIT_SUBMIT_REPO_T6Y not in __CONFIG_JSON:
            LOGGER.error(
                f'请补充配置"{__CONFIG_KEY_GERRIT_SUBMIT_REPO_T6Y}"到.config\n'
            )
        __CONFIG_VALUE_GERRIT_SUBMIT_REPO_T6Y = __CONFIG_JSON[
            __CONFIG_KEY_GERRIT_SUBMIT_REPO_T6Y
        ]
    return __CONFIG_VALUE_GERRIT_SUBMIT_REPO_T6Y


__CONFIG_KEY_HOST_CSC_CONFLUENCE = "host_csc_confluence"
__CONFIG_VALUE_HOST_CSC_CONFLUENCE = None


def get_host_csc_confluence() -> bool:
    global __CONFIG_VALUE_HOST_CSC_CONFLUENCE
    if __CONFIG_VALUE_HOST_CSC_CONFLUENCE == None:
        if __CONFIG_KEY_HOST_CSC_CONFLUENCE not in __CONFIG_JSON:
            LOGGER.error(f'请补充配置"{__CONFIG_KEY_HOST_CSC_CONFLUENCE}"到.config\n')
        __CONFIG_VALUE_HOST_CSC_CONFLUENCE = __CONFIG_JSON[
            __CONFIG_KEY_HOST_CSC_CONFLUENCE
        ]
    return __CONFIG_VALUE_HOST_CSC_CONFLUENCE


__CONFIG_KEY_HOST_REMOTE = "host_remote"
__CONFIG_VALUE_HOST_REMOTE = None


def get_host_remote() -> bool:
    global __CONFIG_VALUE_HOST_REMOTE
    if __CONFIG_VALUE_HOST_REMOTE == None:
        if __CONFIG_KEY_HOST_REMOTE not in __CONFIG_JSON:
            LOGGER.error(f'请补充配置"{__CONFIG_KEY_HOST_REMOTE}"到.config\n')
        __CONFIG_VALUE_HOST_REMOTE = __CONFIG_JSON[__CONFIG_KEY_HOST_REMOTE]
    return __CONFIG_VALUE_HOST_REMOTE


__CONFIG_KEY_GITHUB_OWNERE = "github_owner"
__CONFIG_VALUE_GITHUB_OWNERE = None


def get_github_owner() -> bool:
    global __CONFIG_VALUE_GITHUB_OWNERE
    if __CONFIG_VALUE_GITHUB_OWNERE == None:
        if __CONFIG_KEY_GITHUB_OWNERE not in __CONFIG_JSON:
            LOGGER.error(f'请补充配置"{__CONFIG_KEY_GITHUB_OWNERE}"到.config\n')
        __CONFIG_VALUE_GITHUB_OWNERE = __CONFIG_JSON[__CONFIG_KEY_GITHUB_OWNERE]
    return __CONFIG_VALUE_GITHUB_OWNERE


__CONFIG_KEY_SYNC_JIRA_CONFIG = "sync_jira_config"
__CONFIG_VALUE_SYNC_JIRA_CONFIG = None


def get_sync_jira_config() -> dict:
    global __CONFIG_VALUE_SYNC_JIRA_CONFIG
    if __CONFIG_VALUE_SYNC_JIRA_CONFIG == None:
        if __CONFIG_KEY_SYNC_JIRA_CONFIG not in __CONFIG_JSON:
            LOGGER.error(f'请补充配置"{__CONFIG_KEY_SYNC_JIRA_CONFIG}"到.config\n')
        __CONFIG_VALUE_SYNC_JIRA_CONFIG = __CONFIG_JSON[__CONFIG_KEY_SYNC_JIRA_CONFIG]
    return __CONFIG_VALUE_SYNC_JIRA_CONFIG


__CONFIG_KEY_JIRA_USERS = "jira_users"
__CONFIG_VALUE_JIRA_USERS = None


def get_jira_users() -> dict:
    global __CONFIG_VALUE_JIRA_USERS
    if __CONFIG_VALUE_JIRA_USERS == None:
        if __CONFIG_KEY_JIRA_USERS not in __CONFIG_JSON:
            LOGGER.error(f'请补充配置"{__CONFIG_KEY_JIRA_USERS}"到.config\n')
        __CONFIG_VALUE_JIRA_USERS = __CONFIG_JSON[__CONFIG_KEY_JIRA_USERS]
    return __CONFIG_VALUE_JIRA_USERS


__CONFIG_KEY_WORKLOG_CONFIG = "worklog_config"
__CONFIG_VALUE_WORKLOG_CONFIG = None


def get_worklog_config() -> dict:
    global __CONFIG_VALUE_WORKLOG_CONFIG
    if __CONFIG_VALUE_WORKLOG_CONFIG == None:
        if __CONFIG_KEY_WORKLOG_CONFIG not in __CONFIG_JSON:
            LOGGER.error(f'请补充配置"{__CONFIG_KEY_WORKLOG_CONFIG}"到.config\n')
        __CONFIG_VALUE_WORKLOG_CONFIG = __CONFIG_JSON[__CONFIG_KEY_WORKLOG_CONFIG]
    return __CONFIG_VALUE_WORKLOG_CONFIG


__CONFIG_KEY_MODULES_INFO = "modules_info"
__CONFIG_VALUE_MODULES_INFO = None


def get_modules_info() -> dict:
    global __CONFIG_VALUE_MODULES_INFO
    if __CONFIG_VALUE_MODULES_INFO == None:
        if __CONFIG_KEY_MODULES_INFO not in __CONFIG_JSON:
            LOGGER.error(f'请补充配置"{__CONFIG_KEY_MODULES_INFO}"到.config\n')
        __CONFIG_VALUE_MODULES_INFO = __CONFIG_JSON[__CONFIG_KEY_MODULES_INFO]
    return __CONFIG_VALUE_MODULES_INFO


__CONFIG_KEY_PROJECTS_INFO = "projects_info"
__CONFIG_VALUE_PROJECTS_INFO = None


def get_projects_info() -> dict:
    global __CONFIG_VALUE_PROJECTS_INFO
    if __CONFIG_VALUE_PROJECTS_INFO == None:
        if __CONFIG_KEY_PROJECTS_INFO not in __CONFIG_JSON:
            LOGGER.error(f'请补充配置"{__CONFIG_KEY_PROJECTS_INFO}"到.config\n')
        __CONFIG_VALUE_PROJECTS_INFO = __CONFIG_JSON[__CONFIG_KEY_PROJECTS_INFO]
    return __CONFIG_VALUE_PROJECTS_INFO
