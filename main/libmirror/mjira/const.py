__API_VERSION = 1

from mconfig import get_host_sony


HOST_SONY = get_host_sony()
API_JIRA = "/rest/api/2/"


class API:

    # Format: Host + Api + End
    END_SERVER_INFO = "serverInfo"
    END_PROJECT = "project"
    END_ISSUE = "issue/{}"
    END_ISSUE_CHANGELOG = "issue/{}?expand=changelog"
    END_ISSUE_WORKLOG = "issue/{}/worklog"
    END_ISSUE_ATTACHMENT = "issue/{}?fields=attachment"
    END_SEARCH = "search?jql={}&maxResults=-1"
    END_SEARCH_PARAMS = "search?jql={jql}&fields={fields}&maxResults={max_results}"
    END_SEARCH_CHANGELOG_SPLITED = (
        "search?jql={jql}&expand=changelog&startAt={start_at}&maxResults={max_results}"
    )
    END_SEARCH_SPLITED = "search?jql={jql}&startAt={start_at}&maxResults={max_results}"
    END_BROWSE = "/browse/{}"
    END_CREATE = "issue"
    END_TRANSITIONS = "transitions"
    END_ISSUELINK = "issueLink"
    END_DEL_ATTACHMENT = "attachment/{}"
    END_CREATE_FIXVERSION = "version"
    END_GET_CSC_FIX_VERSIONS = "project/CHINAUX/versions"

    @staticmethod
    def _url(host, path):
        return f"{host}{API_JIRA}{path}"

    SONY_ISSUE = _url.__func__(HOST_SONY, END_ISSUE)
    SONY_SEARCH = _url.__func__(HOST_SONY, END_SEARCH)
    SONY_SEARCH_PARMAS = _url.__func__(HOST_SONY, END_SEARCH_PARAMS)
    SONY_SEARCH_CHANGELOG_SPLITED = _url.__func__(
        HOST_SONY, END_SEARCH_CHANGELOG_SPLITED
    )

class FILTER:
    TOKYO_KEY = (
        '"External JIRA" = "'
        + HOST_SONY
        + '/browse/{0}" or "Child JIRA" = "'
        + HOST_SONY
        + '/browse/{0}"'
    )
    EXTERNAL_KEY = '"External JIRA" = "' + HOST_SONY + '/browse/{0}"'
    CHILD_KEY = '"Child JIRA" = "' + HOST_SONY + '/{0}"'
    INTERNAL_KEY = '"Internal JIRA" = "' + HOST_SONY + '/browse/{}"'
    TRD_KEY = '"3rd-party bug ID" ~ {}'


# Some fields are specific to CSC but not separated here to avoid complexity.
class FIELD:
    ID = "id"
    PROJECT = "project"
    TOTAL = "total"
    ISSUES = "issues"
    ISSUETYPE = "issuetype"
    KEY = "key"
    FIELDS = "fields"
    ASSIGNEE = "assignee"
    ISSUE_LINKS = "issuelinks"
    OUTWARD_ISSUE = "outwardIssue"
    INWARD_ISSUE = "inwardIssue"
    SUMMARY = "summary"
    PRIORITY = "priority"
    NAME = "name"
    TYPE = "type"
    VALUE = "value"
    COMPONENTS = "components"
    FIX_VERSIONS = "fixVersions"
    STATUS = "status"
    DESCRIPTION = "description"
    TRANSITION = "transition"
    CREATED = "created"
    UPDATED = "updated"
    COMMENT = "comment"
    LABELS = "labels"
    RESOLUTION = "resolution"
    DUEDATE = "duedate"
    RESOLUTION_DATE = "resolutiondate"
    CHANGELOG = "changelog"
    HISTORYS = "histories"
    ENVIRONMENT = "environment"
    SUBTASKS = "subtasks"
    WORKLOG = "worklog"
    WORKLOGS = "worklogs"
    AUTHOR = "author"
    STARTED = "started"
    TIMESPENTSECONDS = "timeSpentSeconds"
    ITEMS = "items"
    TO_STRING = "toString"
    FIELD = "field"
    SELF = "self"
    FROM_STRING = "fromString"
    TO_STRING = "toString"
    PARENT = "parent"
    ATTACHMENT = "attachment"


class FIELD_CSC(FIELD):
    RELEASED_PACKAGE_VERSION = "customfield_13260"
    DEVELOPER = "customfield_10420"
    DEFECT_RANK = "customfield_14266"
    CODE_LABELS = "customfield_12876"
    PARENT_ID = "customfield_13960"
    BOC_TEST_RESULT_FILENAME = "customfield_12882"
    BOC_VERIFY_CONCLUSION = "customfield_13170"  # PASS OR FAILED
    BOC_VERIFY_RESULT = "customfield_12886"
    EXTERNAL_JIRA = "customfield_12895"
    DEVELOPER = "customfield_10420"
    TRDID = "customfield_13660"
    IMPACT_SCOPE = "customfield_12871"
    RELEASE_JIRA_ID = "customfield_12875"
    TO_BE_INFORMED = "customfield_10406"
    TASK_JIRA_ID = "customfield_12885"
    SUBMIT_BRANCH = "customfield_12868"
    RELEASE_NOTE_LINK = "customfield_12878"
    DQA_TEST_RESULT_FILENAME = "customfield_12879"
    PULL_REQUEST = "customfield_12872"
    DQA_VERIFY_CONCLUSION = "customfield_12880"
    DEVELOPER_TEST_RESULT_FILE_NAME = "customfield_12890"
    BUG_JIRA_ID = "customfield_14062"
    MODIFICATION_POINTS = "customfield_12867"
    WEEKLY_REPORT = "customfield_12894"
    INTERNAL_JIRA = "customfield_14060"
    CHILD_JIRA = "customfield_14061"
    RESOLVED_VERSION = "customfield_10819"


class FIELD_SONY(FIELD):
    RELEASED_PACKAGE_VERSION = "customfield_29900"
    DETECTED_SW_PROJECT = "customfield_38300"
    ACTION_PLAN = "customfield_14900"
    DETECTED_VERSION = "customfield_10710"
    DEFECT_INFO = "customfield_10708"
    DEFECT_RANK_AUTO = "customfield_31801"
    EXTERNAL_ISSUE_ID = "customfield_17000"


class PROJECT:
    DQA = "CNUXBTRACK"
    CHINAUX = "CHINAUX"


class PROJECT_ID:
    CHINAUX = "11180"
    CNUXDQID = "63200"


class ISSUE_TYPE:
    BUG = "Bug"
    TASK = "Task"
    RELEASE = "Release"
    MT = "Modification Task"
    TODO = "Todo"
    SUB_TASK = "Sub-task"
    CHANGE_SPEC = '"Change Spec"'
    CHILD = "Child"


class PRIORITY:
    CRITICAL = "Critical"
    MAJOR = "Major"
    MINOR = "Minor"
    TBD = "TBD"
    NA = "N/A"


class STATUS:
    OPEN_INTERNAL = "OPEN"
    OPEN_EXTERNAL = "Open"
    REOPENED = "Reopened"
    ASSIGNED = "Assigned"
    INVESTIGATING = "Investigating"
    REPRODUCING = "Reproducing"
    IN_PROGRESS = "IN PROGRESS"
    RESOLVED = "Resolved"
    RELEASED = "Released"
    VERIFIED = "Verified"
    CLOSED = "Closed"
    DQA_VERIFYING = "DQA Verifying"
    FL_JUDGE_DQA = "FL Judge DQA"
    BOC_VERIFYING = "BoC Verifying"
    FL_JUDGE_BOC = "FL Judge BoC"
    IMPLEMENTING = "Implementing"
    WAIT_FOR_REVIEW = "Wait for Review"
    PREPARE_FOR_SUBMIT = "Prepare for Submit"
    DEFERRED = "Deferred"


class TRANSITION:
    REOPEN = "Reopen Issue"
    RESOLVE = "Resolve Issue"
    RESOLVE_MT = "Resolve"
    ASSIGN = "Assign"
    DQA_VERIFY = "DQA Verify"
    FL_JUDGE_DQA = "FL Judge DQA"
    GO = "Go"
    FL_JUDGE_BOC = "FL Judge BoC"
    CLOSED = "Closed"
    START_PROGRESS = "Start Progress"
    APPLY_FOR_REVIEW = "Apply for Review"
    PASS = "Pass"
    RELEASED = "Released"
    CLOSE_ISSUE = "Close Issue"


class LABEL:
    TRD = "ThirdParty"
    CSC = "CSC"
    CSC_RELEASED = "CSC-Released"
    RC_RC = "RC-RC"
    RC_EXTERNAL = "RC-External"
    AUTO = "Auto"


class RESOLUTION:
    FIXED = "Fixed"
    DEFERRED = "Deferred"


class ISSUELINK:
    SYNC = "Synchronizes"
    RELATES1 = "1.Relates"
    RELATES = "Relates"
    CLONE = "Cloners"
    DUPLICATE = "Duplicate"
    BLOCK = "Blocks"
    SPLIT = "Issue split"
