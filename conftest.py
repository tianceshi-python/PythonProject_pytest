# pytest 全局夹具（登录、全局Session）

import hmac
import hashlib
import base64
import os
from _pytest.nodes import Item
import subprocess
from common.email_sender_html import EmailSender

from _pytest.mark.structures import Mark

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ALLURE_RESULTS = os.path.join(BASE_DIR, "allure_results")
REPORT_DIR = os.path.join(BASE_DIR, "reports", "allure_report")
ALLURE_REPORT_PATH = os.path.join(REPORT_DIR, "index.html")

HTML_REPORT_PATH = os.path.join(BASE_DIR, "reports", "test_report.html")

# 全局字典：存储用例标记 + 负责人
CASE_CACHE = {}

"""
def pytest_sessionfinish(session, exitstatus):
    # 所有用例执行完成后自动生成 allure 报告
    print("\n===== 所有用例执行完成，开始生成报告 =====")
    cmd = [
        "allure", "generate",
        ALLURE_RESULTS,
        "-o", REPORT_DIR,
        "--clean"
    ]
    subprocess.run(cmd, cwd=BASE_DIR, check=True)
    print(f"✅ 报告生成完成，路径：{REPORT_DIR}/index.html")
    
    # 调用邮件类，自动发送报告
    # email = EmailSender()
    # email.send_report(ALLURE_REPORT_PATH)
"""


def pytest_collection_modifyitems(items: list[Item]):
    """
    用例收集阶段（执行最早）：统一抓取 标签、用例负责人
    优势：不受pytest版本影响，稳定读取类属性与标记
    """
    for item in items:
        node_id = item.nodeid
        # 1. 提取当前用例所有pytest标记（优先级/模块标签）
        mark_list = [mark.name for mark in item.iter_markers()]
        # 2. 提取用例类上的 case_owner 负责人
        case_owner = ""
        if hasattr(item, "cls") and hasattr(item.cls, "case_owner"):
            case_owner = item.cls.case_owner.strip()

        # 存入全局缓存，后续报告渲染直接读取
        CASE_CACHE[node_id] = {
            "marks": mark_list,
            "owner": case_owner
        }


def pytest_sessionfinish(session, exitstatus):
    """pytest 会话结束后执行"""
    print("\n" + "=" * 60)
    print(f"📄 测试报告已生成：{HTML_REPORT_PATH}")
    print("=" * 60)

    # 调用邮件类，自动发送报告
    # email = EmailSender()
    # email.send_report(HTML_REPORT_PATH)


# 2. 可选：拆分优先级单独一列，更方便筛选
def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>负责人</th>")
    cells.insert(3, "<th>优先级</th>")
    cells.insert(4, "<th>业务模块</th>")

def pytest_html_results_table_row(report, cells):
    case_data = CASE_CACHE.get(report.nodeid, {"marks": [], "owner": ""})
    # marks = case_data["marks"]
    owner = case_data["owner"]

    priority = ""
    module_tag = []
    # 兼容方案：提取用例标签（适配不同pytest版本）
    if hasattr(report, 'iter_markers'):
        # pytest >= 7.0 版本
        marks = list(report.iter_markers())
    elif hasattr(report, 'keywords'):
        # pytest < 7.0 版本
        marks = [k for k in report.keywords if
                 k in ["p0", "p1", "p2", "p3", "geocode", "direction", "smoke", "regression"]]
    else:
        marks = []

    # 遍历标签分类
    for mark in marks:
        # 兼容mark对象和字符串两种格式
        mark_name = mark.name if hasattr(mark, 'name') else mark
        if mark_name in ["p0", "p1", "p2", "p3"]:
            priority = mark_name.upper()
        elif mark_name not in ["smoke", "regression"]:
            module_tag.append(mark_name)

    # 和表头 insert 顺序严格对应
    cells.insert(2, f"<td>{owner if owner else '无'}</td>")
    cells.insert(3, f"<td>{priority}</td>")
    cells.insert(4, f"<td>{','.join(module_tag) if module_tag else '无'}</td>")