import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import time
import base64
from email.header import Header


class EmailSender:
    def __init__(self):
        # QQ邮箱配置
        self.smtp_server = "smtp.qq.com"  # 以 QQ 邮箱为例
        self.smtp_port = 465
        # self.smtp_port = 587
        self.sender = "1192923936@qq.com"
        self.auth_code = "ghwinamnfvfhghhi"  # 不是登录密码，是SMTP授权码
        self.receivers = ["18292813262@163.com"]
        self.nickname = "接口自动化测试"

    def send_report(self, report_path):
        """发送HTML报告附件"""
        # 判断报告文件是否存在
        if not os.path.isfile(report_path):
            print(f"[警告] 报告文件不存在：{report_path}，跳过邮件发送")
            return

        # 组装邮件
        msg = MIMEMultipart()
        # msg["From"] = f"接口自动化测试 <{self.sender}>"
        # msg["From"] = Header(self.nickname, "utf-8") + f" <{self.sender}>"
        nickname_header = Header(self.nickname, "utf-8").encode()
        msg["From"] = f"{nickname_header} <{self.sender}>"
        msg["To"] = ",".join(self.receivers)
        msg["Subject"] = "【接口自动化】测试执行报告" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 邮件正文
        body = "<p>所有接口用例执行完毕，附件为本次测试报告，请查收。</p>"
        msg.attach(MIMEText(body, "html", "utf-8"))

        # 构建附件（标准写法，解决附件识别/乱码问题）,绑定报告为附件
        try:
            with open(report_path, "rb") as f:
                attach = MIMEApplication(f.read(), subtype="octet-stream")
                # 声明附件下载名称，解决中文乱码
                filename = "接口测试报告.html"
                # content_disposition = f"attachment; filename*=utf-8''{filename}"
                # attach.add_header("Content-Disposition", content_disposition)
                filename = filename.encode("utf-8").decode("latin-1")
                attach.add_header("Content-Disposition", "attachment", filename=filename.encode("utf-8").decode("latin-1"))
                # 正确绑定附件
                msg.attach(attach)
                # f.close()
        except PermissionError:
            print("[错误] 无文件读取权限，发送失败")
            return
        except Exception as e:
            print(f"[错误] 读取报告文件异常：{str(e)}")
            return

        # 发送邮件
        try:
            smtp_conn = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, timeout=10)
            # smtp_conn.starttls()  #587端口
            smtp_conn.login(self.sender, self.auth_code)
            smtp_conn.sendmail(self.sender, self.receivers, msg.as_string())
            smtp_conn.quit()
            print("✅ 邮件发送成功！")

        except smtplib.SMTPAuthenticationError:
            print("❌ 认证失败：请检查QQ邮箱授权码是否正确、SMTP服务是否开启")
        except (smtplib.SMTPConnectError, TimeoutError):
            print("❌ 连接失败：网络异常、端口被拦截，请切换网络（如手机热点）重试")
        except Exception as e:
            print(f"❌ 邮件发送失败,位置错误：{str(e)}")
