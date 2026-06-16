# pytest 全局夹具（登录、全局Session）

import hmac
import hashlib
import base64
import os
import subprocess
from common.email_sender_html import EmailSender

from _pytest.mark.structures import Mark

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ALLURE_RESULTS = os.path.join(BASE_DIR, "allure_results")
REPORT_DIR = os.path.join(BASE_DIR, "reports", "allure_report")
ALLURE_REPORT_PATH = os.path.join(REPORT_DIR, "index.html")

HTML_REPORT_PATH = os.path.join(BASE_DIR, "reports", "test_report.html")

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


def pytest_sessionfinish(session, exitstatus):
    """pytest 会话结束后执行"""
    print("\n" + "=" * 60)
    print(f"📄 测试报告已生成：{HTML_REPORT_PATH}")
    print("=" * 60)

    # 调用邮件类，自动发送报告
    # email = EmailSender()
    # email.send_report(HTML_REPORT_PATH)


# 1. HTML报告新增自定义列：展示当前用例全部标签
def pytest_html_results_table_header(cells):
    # 在报告表格新增一列「用例标签」
    cells.insert(2, "<th>Case Tags</th>")

def pytest_html_results_table_row(report, cells):
    tags = []
    # 提取当前用例所有mark标签
    for mark in report.user_marks:
        mark_name = mark.name
        tags.append(f"<span style='color:#0066cc'>{mark_name}</span>")
    tag_html = ", ".join(tags) if tags else "无"
    cells.insert(2, f"<td>{tag_html}</td>")

# 2. 可选：拆分优先级单独一列，更方便筛选
def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>优先级</th>")
    cells.insert(3, "<th>业务模块</th>")

def pytest_html_results_table_row(report, cells):
    priority = ""
    module_tag = []
    for mark in report.user_marks:
        name = mark.name
        if name in ["p0", "p1", "p2", "p3"]:
            priority = name.upper()
        elif name not in ["p0", "p1", "p2", "p3", "smoke", "regression"]:
            module_tag.append(name)
    cells.insert(2, f"<td>{priority}</td>")
    cells.insert(3, f"<td>{','.join(module_tag)}</td>")