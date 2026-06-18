from common.requests_client import RequestsClient
from common.file_reader import read_yaml
from common.logger import logger
from common.assert_tools import AssertTools
from common.base_case import BaseCaseTags

KEY = read_yaml("config/base_config.yaml")["key"]


class DirectionBases(RequestsClient,BaseCaseTags):
    def direction_walking(self, origin, destination, origin_id=None, destination_id=None, callback=None, sig=None,
                          output=None):
        """地理编码"""
        api_data = read_yaml("api/v3/direction_walking.yaml")
        api_path = api_data["url"]
        param = {
            'key': KEY,
            'origin': origin,
            'destination': destination,
            'origin_id': origin_id,
            'destination_id': destination_id,
            'sig': sig,
            'output': output,
            'callback': callback
        }
        rsp, cost_ms = self.send_request(method="GET", api_path=api_path, params=param)
        # 校验请求返回状态码
        AssertTools.assert_status_code(rsp.status_code)
        # 校验请求响应时间
        AssertTools.check_response_time(cost_ms=cost_ms)
        logger.info(f"请求成功：{api_path} | 响应内容：{rsp}")
        return rsp

    def direction_transit(self, location, poitype=None, radius=None, extensions=None, roadlevel=None, sig=None,
                          batch=None,
                          callback=None, homeorcorp=None):
        """逆地理编码"""
        api_data = read_yaml("api/v3/regeo.yaml")
        api_path = api_data["url"]
        print(api_path)
        param = {
            'key': KEY,
            'location': location,
            'poitype': poitype,
            'radius': radius,
            'extensions': extensions,
            'roadlevel': roadlevel,
            'sig': sig,
            'batch': batch,
            'callback': callback,
            'homeorcorp': homeorcorp

        }
        rsp, cost_ms = self.send_request(method="GET", api_path=api_path, params=param)
        # 校验请求返回状态码
        AssertTools.assert_status_code(rsp.status_code)
        # 校验请求响应时间
        AssertTools.check_response_time(cost_ms=cost_ms)
        logger.info(f"请求成功：{api_path} | 响应内容：{rsp.json}")
        return rsp


if __name__ == "__main__":
    Bases = DirectionBases()
    origin = '108.887221,34.214312'
    destination = '108.914404,34.211750'
    rsp = Bases.direction_walking(origin,destination)
    print(rsp)
    data = rsp.json()
    print(data)

