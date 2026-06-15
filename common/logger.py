import logging
import os
from datetime import datetime

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
log_dir = os.path.join(BASE_DIR, "logs")
# 不存在则创建日志目录
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

# 日志文件名称：按日期命名
log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}.log")
# 日志格式：时间-文件名-行号-级别-内容
log_format = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s"

# 日志基础配置
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# 对外暴露日志实例
logger = logging.getLogger()