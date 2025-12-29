import sys
import os
if getattr(sys, "frozen", False):
    # Running in a PyInstaller bundle
    base_path = sys._MEIPASS
else:
    # Running in a normal Python environment
    current_dir = os.path.dirname(os.path.abspath(__file__))
    lib_path = os.path.join(current_dir, 'libmirror')
    sys.path.append(lib_path)

from mjira.const import FIELD_CSC, FIELD_SONY
import mjira.field
from mlogger import LOGGER
import os
import mjira.issue
import mjira.net_sony
import mzendao.trans
import mzendao.net
import mconfig
from openpyxl import load_workbook


def __download_jira_attachments(jira_info, jira_id):
    attachments = mjira.field.get_attachments(jira_info)
    assets_path_list = []
    assets_folder = os.getcwd() + "\\" + jira_id + "\\"
    for attachment_info in attachments:
        mjira.net_sony.download_sony_attachment(
            attachment_info["content"], attachment_info["filename"], assets_folder
        )
        assets_path_list.append(assets_folder + attachment_info["filename"])
    return assets_path_list


# 增加了assignee_name,因为增加了指派人name
def __sync_jira_to_zentao(jira_id, zt_pid, assignee_name):
    try:
        # 获取Jira信息
        sync_result = ""
        input_bug_str = jira_id
        sony_jira_id = ""
        sync_success = "Success"
        sync_fail = "Fail"
        # 是否为DQA Jira Ticket
        input_key_str = mjira.issue.extract_internal_bug_key(input_bug_str)
        if not input_key_str:
            sync_result = jira_id + " - 输入值不为有效的 DQA Jira Ticket"
            return sync_fail, sync_result
        jira_info = mjira.net_sony.get_sony_jira(input_key_str)
        if not input_key_str:
            sync_result = jira_id + " - Sony Jira Center中搜索不到DQA Jira对应的信息"
            return sync_fail, sync_result
        sony_jira_id = input_key_str

        # 转换成Zt参数，传递assignee_name
        zt_id, zt_params = mzendao.trans.trans_sqa_to_zt_home(zt_pid, jira_info, assignee_name)
        if zt_id:
            sync_result = jira_id + " - 此票已存在禅道ID: " + zt_id
            return sync_fail, sync_result
        
        # 获取附件并加载到本地
        assets_path_list = __download_jira_attachments(jira_info, sony_jira_id)
        LOGGER.debug("附件列表:" + str(assets_path_list))
        
        # 创建Zt, 此时应获得Zt Id
        add_result, add_zt_id = mzendao.net.add_bug(zt_params, assets_path_list)
        if not add_result:
            sync_result = "禅道创建失败!"
            if not add_zt_id:
                sync_result = "禅道创建成功, 但获取创建的禅道Id失败!"
            return sync_fail, sync_result
        sync_result = "已创建的禅道："+ add_zt_id
        LOGGER.debug("创建的禅道Id: " + str(add_zt_id))
        
        chandao_link = mjira.issue.format_chandao_link("禅道-" + add_zt_id)
        update_result = mjira.net_sony.update_sony_jira(
                sony_jira_id, {FIELD_SONY.EXTERNAL_ISSUE_ID: chandao_link}
            )
        if update_result:
            sync_result = "禅道" + add_zt_id + "已更新到Jira的Trd Party Id字段"
            print("已将禅道链接更新到Jira的Trd Party Id字段")
            return sync_success, sync_result
        else:
            sync_result = sync_fail, "禅道" + add_zt_id + "更新到Jira失败!"
            return sync_fail, sync_result
    except Exception as e:
        print(e)
        return sync_fail, str(e)
        
if __name__ == "__main__":
    
    # 文件路径
    file_path = mconfig.get_issue_list_file_path()
    
    # 一份读取值
    wb_data = load_workbook(file_path, data_only=True)
    ws_data = wb_data.active
    
    # 一份读取公式
    wb = load_workbook(file_path)
    ws = wb.active
    
    # 处理
    # 读取到D列指派人，写入到G列
    for i, (row_data, row) in enumerate(zip(ws_data.iter_rows(min_row=2, max_col=4),
                                            ws.iter_rows(min_row=2, max_col=7)), start=2):
        jira_id = row_data[0].value  # A列
        module_name = row_data[1].value # B列 模块名称
        zt_pid = str(row_data[2].value)  # C列
        assignee_name = row_data[3].value  # D列：指派人名字
    
        if not jira_id:
            break

        # 如果指派人Name为空，则使用默认指派人
        if not assignee_name:
            assignee_name = mconfig.get_db_manager()  # 使用其他默认值

        # 传递assignee_name
        sync_flg, sync_result = __sync_jira_to_zentao(jira_id, zt_pid, assignee_name)
    
        row[5].value = sync_flg # F列：同步结果
        row[6].value = sync_result # G列：备注
    
    # 保存（保留原始公式）
    wb.save(file_path)
