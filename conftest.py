# pytest 全局夹具（登录、全局Session）

import hmac
import hashlib
import base64
import os
import subprocess
from common.email_sender_html import EmailSender

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ALLURE_RESULTS = os.path.join(BASE_DIR, "allure_results")
REPORT_DIR = os.path.join(BASE_DIR, "reports", "allure_report")

HTML_REPORT_PATH = os.path.join(BASE_DIR, "reports", "test_report.html")




def pytest_sessionfinish(session, exitstatus):
    # 所有用例执行完成后自动生成 allure 报告
    # print("\n===== 所有用例执行完成，开始生成报告 =====")
    # cmd = [
    #     "allure", "generate",
    #     ALLURE_RESULTS,
    #     "-o", REPORT_DIR,
    #     "--clean"
    # ]
    # subprocess.run(cmd, cwd=BASE_DIR, check=True)
    # print(f"✅ 报告生成完成，路径：{REPORT_DIR}/index.html")
    """pytest 会话结束后执行"""
    print("\n" + "=" * 60)
    print(f"📄 测试报告已生成：{HTML_REPORT_PATH}")
    print("=" * 60)

    # 调用邮件类，自动发送报告
    # email = EmailSender()
    # email.send_report(HTML_REPORT_PATH)

    



def sign(secretId, secretKey, httpMethod, headerNonce, headerTimestamp, requestUri, requestBody):
    tobeSig = "{0}\nX-TC-Key={1}&X-TC-Nonce={2}&X-TC-Timestamp={3}\n{4}\n{5}".format(
        httpMethod, secretId,  headerNonce,  headerTimestamp,  requestUri,  requestBody)
    signature = hmac.new(secretKey.encode(
        'utf-8'), tobeSig.encode('utf-8'), digestmod='sha256').hexdigest()
    return base64.b64encode(signature.encode('utf-8'))