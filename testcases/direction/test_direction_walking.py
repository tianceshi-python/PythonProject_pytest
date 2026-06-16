from testcases.direction.direction_bases import DirectionBases
import pytest
from common.assert_tools import AssertTools
from common.file_reader import read_yaml


cases_data = read_yaml("cases_data/direction/walking_case_data.yaml")
normal_case = cases_data["normal"]
error_case = cases_data["error"]


class TestWalkingSuccess(DirectionBases):
    case_owner = "tianxueyan"
    tags = ["direction","p1"]
    timeout = 90

    @pytest.mark.parametrize("item", normal_case, ids=[x["case"] for x in normal_case])
    def test_direction_walking_normal(self, item):
        origin = item["case_params"]["origin"]
        destination = item["case_params"]["destination"]
        rsp = self.direction_walking(origin, destination)
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


class TestWalkingUnnormal(DirectionBases):
    case_owner = "tianxueyan"
    tags = ["direction","p2"]
    timeout = 90

    @pytest.mark.parametrize("item", error_case, ids=[x["case"] for x in error_case])
    def test_direction_walking_unnormal(self, item):
        origin = item["case_params"]["origin"]
        destination = item["case_params"]["destination"]
        rsp = self.direction_walking(origin, destination)
        data = rsp.json()
        # print(data)
        resp_status = data.get("status")
        resp_infocode=data.get("infocode")
        AssertTools.assert_equal(resp_status, item["case_expect"]["status"])
        AssertTools.assert_equal(resp_infocode, item["case_expect"]["infocode"])


if __name__ == "__main__":
    pass
    # pytest.main(["-s", ""])
