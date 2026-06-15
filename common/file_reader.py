import os
import yaml
import json
from common.logger import logger

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# api_path = os.path.join(BASE_DIR, "data")


def read_yaml(file_path):
    """读取yaml文件"""
    full_path = os.path.join(BASE_DIR, file_path)
    # print(full_path)
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data
    except Exception as e:
        logger.error(f"读取YAML文件失败：{str(e)}")
        return None


def read_json(file_path):
    """读取json文件"""
    full_path = os.path.join(BASE_DIR, file_path)
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        logger.error(f"读取JSON文件失败：{str(e)}")
        return None


if __name__ == "__main__":
    print(BASE_DIR)
    # api_path = os.path.join(BASE_DIR, "data")
    # print(api_path)
    # file_path = "v3/geocode.yaml"
    #
    # data = read_yaml(file_path)
    # print(data)

    config_data = read_yaml("config/env_config.yaml")
    print(config_data)
