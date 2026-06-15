import requests
import time
from requests.exceptions import Timeout, ConnectionError, RequestException
from common.logger import logger
from common.file_reader import read_yaml
import settings

# 读取全局配置
config_data = read_yaml("config/env_config.yaml")
ENV = settings.CURRENT_ENV
BASE_URL = config_data["host"][ENV]

# 读取请求重试配置
retry_data = read_yaml("config/loggin_config.yaml")
retry_times = retry_data["retry"]["retry_times"]
retry_interval = retry_data["retry"]["retry_interval"]
requests_timeout = retry_data["retry"]["requests_timeout"]

session = requests.Session()

class RequestsClient:

    # @staticmethod
    def send_request(self, method, api_path, params=None, data=None, json=None, headers=None, retry_times=retry_times,
                     retry_interval=retry_interval, timeout=requests_timeout):
        """
        http请求,统一请求入口
        :param method: 请求方式 GET / POST
        :param api_path: 接口相对路径
        :param params: URL参数
        :param data: 表单参数
        :param json: JSON请求体
        :param headers: 请求头
        :param retry_times: 重试次数
        :param retry_interval: 重试间隔
        :param timeout: 超时时间
        :return: 接口返回rsp 、cost_ms（接口请求耗时）
        """
        url = BASE_URL + api_path
        # 合并请求头
        if headers:
            session.headers.update(headers)

        # 循环重试
        for i in range(retry_times + 1):
            try:
                start_time = time.time()
                if method.upper() == "GET":
                    resp = session.get(url, params=params, timeout=timeout)
                elif method.upper() == "POST":
                    resp = session.post(url, params=params, data=data, json=json, timeout=timeout)
                elif method.upper() == "PUT":
                    resp = session.put(url, params=params, data=data, json=json, timeout=timeout)
                elif method.upper() == "DELETE":
                    resp = session.delete(url, params=params, timeout=timeout)
                else:
                    logger.error(f"不支持的请求方式：{method}")
                    return {"code": -999, "msg": "非法请求方式"}

                logger.info(f"请求方式：{method} | 请求地址：{url} | 请求参数：{params} ｜ 返回响应：{resp} ")
                cost_ms = (time.time() - start_time) * 1000
                logger.info(f"请求耗时：{cost_ms}ms")

                # 捕获4xx/5xx HTTP状态码异常
                resp.raise_for_status()
                logger.info(f"请求成功：{url} | 响应内容：{resp.text}")
                return resp, cost_ms

            except Timeout:
                logger.warning(f"第{i + 1}次请求超时：{url}")
                if i == retry_times:
                    return {"code": -1, "msg": "请求超时，重试次数用尽"}
                time.sleep(retry_interval)
            except ConnectionError:
                logger.error(f"接口连接失败：{url}")
                return {"code": -2, "msg": "服务连接失败"}
            except RequestException as e:
                logger.error(f"请求异常：{str(e)}")
                return {"code": -3, "msg": f"未知异常：{str(e)}"}

    def request(self, method, api_path, params=None, data=None, json=None, headers=None, check=200):
        """
        http请求,封装基本状态码校验
        :param method: 请求方式 GET / POST
        :param api_path: 接口相对路径
        :param params: URL参数
        :param data: 表单参数
        :param json: JSON请求体
        :param headers: 请求头
        :return: 接口返回rsp 、cost_ms（接口请求耗时）
        """
        rsp, cost_ms = self.send_request(method, api_path, params, data, json, headers)
        if rsp.status_code != check:
            logger.error(f"请求失败：{api_path} | 返回响应状态码：{rsp.status_code}")
            return rsp, cost_ms
        return rsp, cost_ms


if __name__ == "__main__":
    # print(BASE_URL)

    api_data = read_yaml("data/v3/geocode.yaml")
    print(api_data)
    api_path = api_data["url"]
    parameters = api_data["parameters"]
    key = read_yaml("config/loggin_config.yaml")["key"]
    parameters["key"] = key
    parameters["address"] = "北京市朝阳区阜通东大街6号"
    print(parameters)
    request_client = RequestsClient()
    data, cost_ms = request_client.request("GET", api_path, params=parameters)
    print(data)
    print(cost_ms)
