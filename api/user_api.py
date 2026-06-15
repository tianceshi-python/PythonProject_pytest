# 用户模块：登录、获取信息
from common.requests_client import RequestsClient

class UserApi:
    @staticmethod
    def login(username, password):
        """登录接口"""
        body = {
            "username": username,
            "password": password
        }
        return RequestsClient.send_request("POST", "/api/user/login", json=body)

    @staticmethod
    def get_user_info():
        """获取用户信息接口（依赖登录Token）"""
        return RequestsClient.send_request("GET", "/api/user/info")