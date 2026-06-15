from common.file_reader import read_yaml


class BaseCase:
    """测试用例公共基类：封装全局前置、后置"""

    # 类级别：整个测试类执行一次
    @classmethod
    def setup_class(cls):
        print("\n【基类-类前置】登录、初始化全局会话")
        # cls.token = "base_token_123"
        pass

    @classmethod
    def teardown_class(cls):
        print("【基类-类后置】销毁会话、清空token")

    # 方法级别：每条用例执行一次
    def setup_method(self):
        print("【基类-用例前置】初始化请求参数、临时数据")
        self.key = read_yaml("config/loggin_config.yaml")["key"]

    def teardown_method(self):
        print("【基类-用例后置】清理临时数据")


# 用例上下文管理
class TestContext:
    def __init__(self):
        self.data = {}  # 动态存储所有链路参数

    def reset(self):
        """统一重置：清空所有临时数据，一条方法适配所有链路"""
        self.data.clear()
