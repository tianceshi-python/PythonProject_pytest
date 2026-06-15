from common.logger import logger
from common.file_reader import read_yaml

max_ms_requests = read_yaml("config/base_config.yaml")["retry"]["max_ms_requests"]


class AssertTools():
    @staticmethod
    def assert_status_code(actual_code, expect_code=200):
        """断言业务状态码"""
        # actual_code = res.get("code")
        assert actual_code == expect_code, f"状态码异常，预期{expect_code}，实际{actual_code}"
        logger.debug("状态码断言通过")

    @staticmethod
    def assert_not_empty(value):
        """断言字段非空"""
        assert value is not None and value != "", "字段为空"
        logger.debug("非空断言通过")

    @staticmethod
    def assert_keyword(content, keyword_list):
        """AI接口专用：关键词断言（数据驱动常用）"""
        for kw in keyword_list:
            assert kw in content, f"返回内容缺失关键词：{kw}"
        logger.debug("关键词断言通过")

    @staticmethod
    def assert_equal(actual_value, expect_value):
        """断言相等"""
        assert actual_value == expect_value, f"值不相等，预期：{expect_value}，实际：{actual_value}"
        logger.debug(f"相等断言通过")

    @staticmethod
    def assert_not_equal(actual_value, expect_value):
        """断言不相等"""
        assert actual_value != expect_value, f"值相等，预期：{expect_value}，实际：{actual_value}"
        logger.debug("不相等断言通过")

    # 响应时间校验
    @staticmethod
    def check_response_time(cost_ms, max_ms=max_ms_requests):
        """断言响应时间"""
        if cost_ms > max_ms:
            logger.info(f"响应时间过长，预期：{max_ms}ms，实际：{cost_ms}ms")
        logger.debug(f"响应时间在设置阈值:{max_ms}范围内")
