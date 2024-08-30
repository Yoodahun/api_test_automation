from typing import Dict

import requests

from src.base_api_client import BaseAPIClient


class Register(BaseAPIClient):

    def __init__(self):
        super().__init__("https://reqres.in")
        self.resource = "api/register"

    @property
    def schema_when_register_id(self) -> dict:
        schema = {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer"
                },
                "token": {
                    "type": "string"
                }
            },
            "required": ["id", "token"]
        }

        return schema

    def register_id(self, user_email=None, password=None) -> requests.Response:
        """
        아이디와 패스워드를 입력받아 등록합니다.
        :param user_email:
        :param password:
        :return: requests.Response
        """
        self.logger.info("register_id 실행")

        data = dict()
        if user_email:
            data["email"] = user_email

        if password:
            data["password"] = password


        return self.post(endpoint=self.resource, data=data)
