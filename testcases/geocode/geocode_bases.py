from common.requests_client import RequestsClient
from common.file_reader import read_yaml
from common.logger import logger
from common.assert_tools import AssertTools

KEY = read_yaml("config/base_config.yaml")["key"]


class GeocodeBases(RequestsClient):
    def geocode_geo(self, address, city=None, sig=None, output=None):
        """地理编码"""
        api_data = read_yaml("data/v3/geocode.yaml")
        api_path = api_data["url"]
        param = {
            'key': KEY,
            'address': address,
            'city': city,
            'output': sig,
            'callback': output
        }
        rsp, cost_ms = self.send_request(method="GET", api_path=api_path, params=param)
        # 校验请求返回状态码
        AssertTools.assert_status_code(rsp.status_code)
        # 校验请求响应时间
        AssertTools.check_response_time(cost_ms=cost_ms)
        logger.info(f"请求成功：{api_path} | 响应内容：{rsp}")
        return rsp

    def geocode_regeo(self, location, poitype=None, radius=None, extensions=None, roadlevel=None, sig=None, batch=None,
                      callback=None, homeorcorp=None):
        """逆地理编码"""
        api_data = read_yaml("data/v3/regeo.yaml")
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
    geo = GeocodeBases()
    rsp = geo.geocode_geo("北京市东城区东长安街天安门广场")
    print(rsp)
    data = rsp.json()
    print(data)
    location = data.get("geocodes")[0]["location"]
    print(location)
    # rsp = geo.geocode_regeo(location)
    # print(rsp.json())
