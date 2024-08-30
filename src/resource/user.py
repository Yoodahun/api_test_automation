import requests

from src.base_api_client import BaseAPIClient


class User(BaseAPIClient):

    def __init__(self):
        super().__init__("https://reqres.in")
        self.resource = "api/users"

    @property
    def schema_when_get_single_user(self) -> dict:
        """
        /api/users 에 대한 스키마를 리턴한다.
        :return: dict
        """
        schema = {
            "type": "object",
            "properties": {
                "data": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "email": {"type": "string", "format": "email"},
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "avatar": {"type": "string", "format": "uri"}
                    },
                    "required": ["id", "email", "first_name", "last_name", "avatar"]
                }
            },
            "required": ["data"]
        }

        return schema

    @property
    def schema_when_user_created(self) -> dict:
        """
        유저 생성했을 때의 스키마를 리턴합니다.
        :return: dict
        """
        schema = {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "pattern": "^[0-9]+$"
                },
                "createdAt": {
                    "type": "string",
                    "format": "date-time"
                }
            },
            "required": ["id", "createdAt"]
        }

        return schema

    def get_list_users(self) -> requests.Response:
        """
        전체 유저 리스트를 반환합니다.
        """
        return self.get(endpoint=self.resource)

    def get_single_user(self, user_id: str) -> requests.Response:
        """
        하나의 유저를 찾아 리턴합니다.
        :param user_id:
        :return:
        """
        return self.get(endpoint=f"{self.resource}/{user_id}")

    def create_a_user(self, user_name: str = "", user_job: str = "") -> requests.Response:
        """
        유저를 생성하고 그 응답값을 반환합니다.
        :param user_name:
        :param user_job:
        :return:
        """
        user_name = user_name if user_name != "" else "Smith"
        user_job = user_job if user_job != "" else "QA engineer"
        data = {
            "name": user_name,
            "job": user_job
        }

        return self.post(endpoint=self.resource, data=data)
