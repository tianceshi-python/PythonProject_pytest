# AI大模型对话接口
from common.requests_client import RequestsClient

class LlmApi:
    @staticmethod
    def chat(prompt):
        """大模型对话接口"""
        body = {"prompt": prompt}
        return RequestsClient.send_request("POST", "/api/llm/chat", json=body)