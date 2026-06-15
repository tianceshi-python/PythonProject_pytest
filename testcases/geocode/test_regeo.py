from testcases.geocode.geocode_bases import GeocodeBases
import pytest
from common.assert_tools import AssertTools
from common.file_reader import read_yaml
import time
import os

cases_data = read_yaml("cases_data/geocode/regeo_case_data.yaml")
normal_case = cases_data["normal"]
error_case = cases_data["error"]


class TestRegeoSuccess(GeocodeBases):
    case_owner = "tianxueyan"
    tag = "geocode_regeo"
    timeout = 90

    @pytest.mark.parametrize("item", normal_case, ids=[x["case"] for x in normal_case])
    def test_regeo_success(self, item):
        location = item["case_params"]["location"]
        print(location)
        rsp = self.geocode_regeo(location)
        data = rsp.json()
        print(data)
        rsp_formatted_address = data.get("regeocode")["formatted_address"]
        print(rsp_formatted_address)
        resp_status = data.get("status")
        AssertTools.assert_equal(resp_status, item["case_expect"]["status"])
        AssertTools.assert_equal(rsp_formatted_address, item["case_expect"]["formatted_address"])


class TestRegeoFail(GeocodeBases):
    case_owner = "tianxueyan"
    tag = "geocode_regeo"
    timeout = 90

    @pytest.mark.parametrize("item", error_case, ids=[x["case"] for x in error_case])
    def test_regeo_fail(self, item):
        location = item["case_params"]["location"]
        rsp = self.geocode_regeo(location)
        data = rsp.json()
        rsp_formatted_address = data.get("regeocode")["formatted_address"]
        print(data)
        resp_status = data.get("status")
        AssertTools.assert_equal(resp_status, item["case_expect"]["status"])
        AssertTools.assert_equal(rsp_formatted_address, item["case_expect"]["formatted_address"])


if __name__ == "__main__":
    # TestRegeoSuccess().test_regeo_success(normal_case[0])
    pytest.main(["-s", os.path.abspath(__file__)])
