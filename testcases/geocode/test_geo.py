from testcases.geocode.geocode_bases import GeocodeBases
import pytest
from common.assert_tools import AssertTools
from common.file_reader import read_yaml
import time

cases_data = read_yaml("cases_data/geocode/geo_case_data.yaml")
normal_case = cases_data["normal"]
error_case = cases_data["error"]


class TestGeoSuccess(GeocodeBases):
    case_owner = "tianxueyan"
    tag = "geocode"
    timeout = 90

    @pytest.mark.parametrize("item", normal_case, ids=[x["case"] for x in normal_case])
    def test_geo_success(self, item):
        address = item["case_params"]["address"]
        rsp = self.geocode_geo(address)
        data = rsp.json()
        resp_status = data.get("status")
        resp_location = data.get("geocodes")[0]["location"]
        AssertTools.assert_equal(resp_status, item["case_expect"]["status"])
        AssertTools.assert_not_empty(resp_location)

class TestGeoFail(GeocodeBases, AssertTools):
    case_owner = "tianxueyan"
    tag = "geocode"
    timeout = 90

    @pytest.mark.parametrize("item", error_case, ids=[x["case"] for x in error_case])
    def test_geo_fail(self, item):
        address = item["case_params"]["address"]
        rsp = self.geocode_geo(address)
        data = rsp.json()
        resp_status = data.get("status")
        resp_infocode = data.get("infocode")
        AssertTools.assert_equal(resp_status, item["case_expect"]["status"])
        AssertTools.assert_equal(resp_infocode, item["case_expect"]["infocode"])


if __name__ == "__main__":
    pytest.main(["-s", "testcases/geocode/test_geo.py"])
