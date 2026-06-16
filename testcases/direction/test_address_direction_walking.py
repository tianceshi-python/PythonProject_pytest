from testcases.direction.direction_bases import DirectionBases
from testcases.geocode.geocode_bases import GeocodeBases
from common.base_case import TestContext
import pytest
from common.assert_tools import AssertTools
from common.file_reader import read_yaml

cases_data = read_yaml("cases_data/direction/address_walking_case_data.yaml")
normal_case = cases_data["normal"]
error_case = cases_data["error"]

context = TestContext()


class TestAddressWalkingSuccess(DirectionBases, GeocodeBases):
    case_owner = "tianxueyan"
    tag = ["direction","p0","smoke"]
    timeout = 90

    @pytest.mark.parametrize("item", normal_case, ids=[x["case"] for x in normal_case])
    def test_address_direction_walking_normal(self, item):
        # ========== 关键：用例执行前重置上下文，实现数据隔离 ==========
        context.reset()

        origin_address = item["case_params"]["origin_address"]
        destination_address = item["case_params"]["destination_address"]

        try:
            #     获取起点经纬度
            origin_rsp = self.geocode_geo(origin_address)
            origin_data = origin_rsp.json()
            origin_location = origin_data.get("geocodes")[0]["location"]
            context.data["origin_location"] = origin_location

            #   获取终点经纬度
            destination_rsp = self.geocode_geo(destination_address)
            destination_data = destination_rsp.json()
            destination_location = destination_data.get("geocodes")[0]["location"]
            context.data["destination_location"] = destination_location

            context_origin_location = context.data["origin_location"]
            context_destination_location = context.data["destination_location"]
            rsp = self.direction_walking(context_origin_location, context_destination_location)
            data = rsp.json()
            print(data)
            resp_status = data.get("status")
            resp_paths = data.get("route")["paths"]
            if len(resp_paths) != 0:
                resp_steps = resp_paths[0]["steps"]
                if len(resp_steps) != 0:
                    resp_instruction = resp_steps[0]["instruction"]
                resp_distance = resp_steps[0]["distance"]
            AssertTools.assert_equal(resp_status, item["case_expect"]["status"])
            AssertTools.assert_not_empty(resp_distance)
            AssertTools.assert_not_empty(resp_instruction)
        except Exception as e:
            pytest.fail(f"用例失败：{item['name']}，原因：{str(e)}")


class TestAddressWalkingUnnormal(DirectionBases, GeocodeBases):
    case_owner = "tianxueyan"
    tag = ["direction","p2"]
    timeout = 90

    @pytest.mark.parametrize("item", error_case, ids=[x["case"] for x in error_case])
    def test_address_direction_walking_unnormal(self, item):
        # ========== 关键：用例执行前重置上下文，实现数据隔离 ==========
        context.reset()

        origin_address = item["case_params"]["origin_address"]
        destination_address = item["case_params"]["destination_address"]

        try:
            #     获取起点经纬度
            origin_rsp = self.geocode_geo(origin_address)
            origin_data = origin_rsp.json()
            if origin_data.get("status") != "1":
                return
            origin_location = origin_data.get("geocodes")[0]["location"]
            context.data["origin_location"] = origin_location

            #   获取终点经纬度
            destination_rsp = self.geocode_geo(destination_address)
            destination_data = destination_rsp.json()
            if destination_data.get("status") != "1":
                return
            destination_location = destination_data.get("geocodes")[0]["location"]
            context.data["destination_location"] = destination_location

            context_origin_location = context.data["origin_location"]
            context_destination_location = context.data["destination_location"]
            rsp = self.direction_walking(context_origin_location, context_destination_location)
            data = rsp.json()
            print(data)
            resp_status = data.get("status")
            resp_infocode = data.get("infocode")
            AssertTools.assert_equal(resp_status, item["case_expect"]["status"])
            AssertTools.assert_equal(resp_infocode, item["case_expect"]["infocode"])

        except Exception as e:
            pytest.fail(f"用例失败：{item['name']}，原因：{str(e)}")


if __name__ == "__main__":
    pass
    # pytest.main(["-s", ""])
