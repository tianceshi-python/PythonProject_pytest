import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import time

class EmailSender:
    def __init__(self):
        self.smtp_server = "smtp.qq.com"  # 以 QQ 邮箱为例
        self.smtp_port = 465
        self.sender = "1192923936@qq.com"
        self.auth_code = "ghwinamnfvfhghhi"  # 不是登录密码，是SMTP授权码
        self.receivers = ["18292813262@163.com"]

    def send_report(self, report_path):
        """发送测试报告"""
        msg = MIMEMultipart()
        msg["From"] = "自动化测试<{}>".format(self.sender)
        msg["To"] = ",".join(self.receivers)
        msg["Subject"] = "【接口自动化】测试执行报告"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 邮件正文
        body = """
        <h3>接口自动化用例执行完成</h3>
        <p>附件为本次测试报告，请查收！</p>
        """
        msg.attach(MIMEText(body, "html", "utf-8"))

        # 附加报告文件
        if os.path.exists(report_path):
            with open(report_path, "rb") as f:
                part = MIMEApplication(f.read(), _subtype="html")
                part.add_header("Content-Disposition", "attachment", filename="test_report.html")
                msg.attach(part)

        # 发送邮件
        try:
            smtp = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            smtp.login(self.sender, self.auth_code)
            smtp.sendmail(self.sender, self.receivers, msg.as_string())
            smtp.quit()
            print("✅ 邮件发送成功！")
        except Exception as e:
            print(f"❌ 邮件发送失败：{e}")