from common.file_reader import read_yaml
from common.test_tags import Tag
import pytest
import allure

# 预加载全部合法标签，用于校验
VALID_TAGS = [val for key, val in Tag.__dict__.items() if not key.startswith("_")]


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


class BaseCaseTags:
    """
    通过tags给用例打标签，并在测试报告中体现
    """
    tags: list[str] = []

    # 类装饰器：自动给所有test方法添加tags标记
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # 取出当前子类定义的tags列表
        tag_list = getattr(cls, "tags", [])
        owner = cls.case_owner.strip() if hasattr(cls, "case_owner") else ""
        # 无标签直接跳过
        if not tag_list:
            return


        # 校验：所有标签必须来自预定义常量，禁止手写自定义字符串
        for tag in tag_list:
            if tag not in VALID_TAGS:
                raise ValueError(f"用例类 {cls.__name__} 包含非法标签[{tag}]，请使用common/test_tags.py的Tag常量")

        # 遍历所有test_开头测试方法，批量叠加标签
        for attr_name in dir(cls):
            func = getattr(cls, attr_name)
            if attr_name.startswith("test_") and callable(func):
                wrap_func = func

                # ========== 自动注入 Allure 负责人 ==========
                # if owner:
                #     wrap_func = allure.owner(owner)(wrap_func)

                # ========== 自动注入 pytest 标签 + Allure 分类/优先级 ==========
                for tag in tag_list:
                    # pytest 用例打标签
                    wrap_func = getattr(pytest.mark, tag)(wrap_func)
                    # Allure 报告标签（核心！）
                    # if tag in ["p0", "p1", "p2", "p3"]:
                    #     wrapped = allure.severity(tag)(wrapped)
                    # elif tag in ["geocode", "direction"]:
                    #     wrapped = allure.feature(tag)(wrapped)
                    # else:
                    #     wrapped = allure.tag(tag)(wrapped)
                setattr(cls, attr_name, wrap_func)