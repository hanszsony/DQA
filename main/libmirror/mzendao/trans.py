__API_VERSION = 1

from typing import List

import re
from mconfig import get_to_zt_bug_section, get_db_manager, get_trans_descriptions

import mjira.field
import mjira.issue

# ------------------------------------------ Zendao Params ---------------------------------------------

"""
params = {
"product": 58 --> const.PRODUCT_ID.x
"openedBuild": ["trunk"], --> 默认值, 代表主干
"assignedTo": "wangchen2", --> const.ASSIGNEE.x
"deadline": "2024-12-21", --> 截止日期, 一般不用
"type": "codeerror", --> 默认值, 类型:代码错误
"os": "windows", --> 平台系统, 一般不用
"browser": "ie11", --> 浏览器版本, 一般不用
"title": "添加bug测试1", --> bug标题
"color": "#2dbdb2", --> 不知含义, 一般不用
"severity": 2, --> 和pri取同一值, 转换自DefectRank
"pri": 1, --> 和severity取同一值, 转换自DefectRank
"steps": "重现步骤描述添加bug测试四", --> 步骤、结果、期望、环境、备注, 直接c
"story": 0, --> 不知含义, 一般不用
"task": 0, --> 不知含义, 一般不用
"keywords": "bug1", --> 关键字, 一般不用
}
"""


class KEY:
    PRODUCT = "product"
    STATUS = "status"
    OPENED_BUILD = "openedBuild"
    ASSIGNED_TO = "assignedTo"
    DEADLINE = "deadline"
    TYPE = "type"
    OS = "os"
    DROWSER = "browser"
    TITLE = "title"
    COLOR = "color"
    SEVERITY = "severity"
    PRIORITY = "pri"
    STEPS = "steps"
    STORY = "story"
    TASK = "task"
    KEYWORDS = "keywords"


class STATUS:
    ACTIVE = "active"  # 激活
    ALL = "all"  # 所有
    UNCLOSED = "unclosed"  # 未关闭
    OPENED_BY_ME = "openedbyme"  # 由我创建
    ASSIGN_TO_ME = "assigntome"  # 指派给我
    RESOLVED_BY_ME = "resolvedbyme"  # 由我解决
    TO_CLOSED = "toclosed"  # 待关闭
    UNRESOLVED = "unresolved"  # 未解决
    UNCONFIRMED = "unconfirmed"  # 未确认
    LONG_LIFE_BUGS = "longlifebugs"  # 久未处理
    POSTPONED_BUGS = "postponedbugs"  # 被延期
    OVERDUE_BUGS = "overduebugs"  # 过期BUG
    NEED_CONFIRM = "needconfirm"  # 需求变动


class OPENED_BUILD:
    TRUNK = "trunk"  # 主干, 需要传入id


class TYPE:
    CODE_ERROR = "codeerror"

PRIORITY_DICT = {1: ["A", "B1"], 2: ["B2"], 3: ["B3"], 4: ["C"]}

ASSIGNEE = get_db_manager()

IS_TRANS_DESCRIPTIONS = get_trans_descriptions()


def __wrap_lines_with_p_tags(message):
    lines = message.split("\n")
    wrapped_lines = [f"<p>{line}</p>" for line in lines]
    return "".join(wrapped_lines)


def __wrap_lines_with_b_tags(message):
    return f"<b>{message}</b>" if message else ""


#def __translate_large_text(text: str, target_language: str = "zh") -> str:
#    from translate import Translator # type: ignore
#    """
#    Translate a large English text into the target language, handling input over 500 characters.
#
#    :param text: The English text to translate
#    :param target_language: The target language code (default is 'zh' for Chinese)
#    :return: The translated text
#    """
#
#    def split_text(text: str, max_length: int = 500) -> List[str]:
#        """Split text into chunks of at most `max_length` characters by `\n`."""
#        parts = text.split("\n")
#        result = []
#        current_chunk = ""
#
#        for part in parts:
#            if len(current_chunk) + len(part) + 1 > max_length:  # +1 for potential '\n'
#                result.append(current_chunk)
#                current_chunk = part
#            else:
#                current_chunk = f"{current_chunk}\n{part}".strip()
#
#        if current_chunk:
#            assert (
#                len(current_chunk) < 500
#            ), "Chunk Size Large than 500, cannot translate"
#            result.append(current_chunk)
#
#        return result
#
#    translator = Translator(to_lang=target_language)
#
#    # Split text into manageable chunks
#    text_chunks = split_text(text)
#
#    # Translate each chunk and concatenate results
#    translated_chunks = [translator.translate(chunk) for chunk in text_chunks]
#
#    return "\n".join(translated_chunks)


def __extract_eng_procedure(text):
    # 正则表达式匹配从 ***Procedure 到下一个 *** 或末尾
    pattern = r"\*\*\*Procedure.*?(?=\*\*\*|$)"
    matches = re.findall(pattern, text, re.DOTALL)
    return "\n".join(matches)


def __extract_cn_procedure(text):
    # 正则表达式匹配从【步骤】或[步骤]到下一个[或【的段落
    pattern = r"[【\[]步骤[】\]](.*?)(?=\[|\【|$)"
    matches = re.findall(pattern, text, re.DOTALL)
    return "\n".join(matches)


def __extract_eng_defective_result(text):
    # 正则表达式匹配从【Symptom Details】或[Symptom Details]到下一个[或【的段落
    pattern = r"[【\[]Symptom Details[】\]](.*?)(?=\[|\【|$)"
    matches = re.findall(pattern, text, re.DOTALL)
    return "\n".join(matches)


def __extract_cn_defective_result(text):
    # 正则表达式匹配从【结果】或[结果]到下一个[或【的段落
    pattern = r"[【\[]结果[】\]](.*?)(?=\[|\【|$)"
    matches = re.findall(pattern, text, re.DOTALL)
    return "\n".join(matches)


def __extract_eng_expected_result(text):
    # 正则表达式匹配从【Expected Result】或[Expected Result]到下一个[或【的段落
    pattern = r"[【\[]Expected Result[】\]](.*?)(?=\[|\【|$)"
    matches = re.findall(pattern, text, re.DOTALL)
    return "\n".join(matches)


def __extract_cn_expected_result(text):
    # 正则表达式匹配从【期望】或[期望]到下一个[或【的段落
    pattern = r"[【\[]期望[】\]](.*?)(?=\[|\【|$)"
    matches = re.findall(pattern, text, re.DOTALL)
    return "\n".join(matches)


def __extract_eng_environment(text):
    # 正则表达式匹配从 ***Environmental Condition 到下一个 *** 或末尾
    pattern = r"\*\*\*Environmental Condition.*?(?=\*\*\*|$)"
    matches = re.findall(pattern, text, re.DOTALL)
    return "\n".join(matches)


def __extract_cn_environment(text):
    # 正则表达式匹配从【环境】或[环境]到下一个[或【的段落
    pattern = r"[【\[]环境[】\]](.*?)(?=\[|\【|$)"
    matches = re.findall(pattern, text, re.DOTALL)
    return "\n".join(matches)


def __extract_eng_note(text):
    # 正则表达式匹配从【Note|Notice|Remarks】或[Note|Notice|Remarks]到下一个[或【的段落
    pattern = r"[【\[](?:Note|Notice|Remarks)[】\]](.*?)(?=\[|\【|$)"
    matches = re.findall(pattern, text, re.DOTALL)
    return "\n".join(matches)


def __extract_cn_note(text):
    # 正则表达式匹配从【备注】或[备注]到下一个[或【的段落
    pattern = r"[【\[](?:备注)[】\]](.*?)(?=\[|\【|$)"
    matches = re.findall(pattern, text, re.DOTALL)
    return "\n".join(matches)


def __get_html_steps(defect_info, detected_version):
    steps = ""

    procedure = __extract_eng_procedure(defect_info)
    if not procedure:
        procedure = __extract_cn_procedure(defect_info)
    procedure = (
        __wrap_lines_with_b_tags("[步骤]") + procedure
    )
    procedure = procedure.replace("Initial Situation", "初始情况")
    procedure = procedure.replace("Operation/State", "操作/状态")

    defective_result = __extract_eng_defective_result(defect_info)
    if not defective_result:
        defective_result = __extract_cn_defective_result(defect_info)
    defective_result = (
        "\n"
        + __wrap_lines_with_b_tags("[结果]")
        + defective_result
    )

    expected_result = __extract_eng_expected_result(defect_info)
    if not expected_result:
        expected_result = __extract_cn_expected_result(defect_info)
    expected_result = (
        "\n"
        + __wrap_lines_with_b_tags("[期望]")
        + expected_result
    )

    environment = __extract_eng_environment(defect_info)
    if not environment:
        environment = __extract_cn_environment(defect_info)
    environment = (
        "\n"
        + __wrap_lines_with_b_tags("[环境]")
        + environment
        + "\nPKG: "
        + detected_version
    )

    note = __extract_eng_note(defect_info)
    if not note:
        note = __extract_cn_note(defect_info)
    note = (
        "\n" + __wrap_lines_with_b_tags("[备注]") + "\n" + note
    )

    steps = (
        procedure
        + defective_result
        + expected_result
        + environment
        + note
        #+ "\n\n\n"
        #+ __wrap_lines_with_b_tags(">>> 原文参考(需删除):")
        #+ defect_info
    )
    steps = steps.replace("***Procedure", "")
    steps = steps.replace("***Environmental Condition", "")
    html_steps = __wrap_lines_with_p_tags(steps)
    return html_steps

# 增加了assignee_name,因为增加了指派人name
def trans_sqa_to_zt_home(zt_pid, jira_json, assignee_name: str = None) -> dict:
    
    external_issue_link = mjira.field.get_external_issue(jira_json)
    zt_id = (
        mjira.issue.extract_chandao_key(external_issue_link.strip())
        if external_issue_link
        else None
    )
    
    if zt_id:
        return zt_id, {}

    title = mjira.field.get_summary(jira_json)
    if not title:
        print(title + " - Error: jira summary is empty")

    priority = 0
    defect_rank = mjira.field.get_defect_rank_auto(jira_json)
    for zt_pri, defect_rank_list in PRIORITY_DICT.items():
        if defect_rank in defect_rank_list:
            priority = zt_pri
            break
    if not priority:
        print(priority + " - Error: defect rank in jira does not match priority dict")

    defect_info = mjira.field.get_defect_info(jira_json)
    if not defect_info:
        print(defect_info + " - Error: defect info not found in jira")
    
    if IS_TRANS_DESCRIPTIONS:
        detected_pkg = mjira.field.get_detected_version(jira_json)
        if detected_pkg: 
            print(detected_pkg + " - Error: detected pkg not found in jira")
        html_steps = __get_html_steps(defect_info, detected_pkg)
    else:
        html_steps = defect_info

    # 校验指派人Name
    if not assignee_name:
        # 使用config中的默认值
        default_assignee = get_db_manager()
        if not default_assignee:
            raise ValueError("Excel中未指定指派人，且config中也没有默认指派人")
        assignee_name = default_assignee

    print(f"DEBUG: 最终使用的指派人Name: {assignee_name}")

    return zt_id, {
        KEY.PRODUCT: zt_pid,
        KEY.STATUS: STATUS.ACTIVE,
        KEY.OPENED_BUILD: [OPENED_BUILD.TRUNK],
        KEY.ASSIGNED_TO: assignee_name, # 使用传入的assignee_name
        KEY.TYPE: TYPE.CODE_ERROR,
        KEY.TITLE: title,
        KEY.SEVERITY: priority,
        KEY.PRIORITY: priority,
        KEY.STEPS: html_steps,
    }
