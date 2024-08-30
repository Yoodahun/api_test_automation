import json

import requests
from helper import get_logger
from jsonschema import validate


class BaseTest:
    """
    테스트 클래스 내에서 기본적으로 많이 쓰일 함수들을 모아놓은 곳.
    """
    logger = get_logger(__name__)

    def convert_json_data(self, response: requests.Response) -> dict:
        """
        입력받은 응답값은 json 데이터로 파싱합니다.
        :param response:
        :return:
        """
        return response.json()

    def validate_response_schema(self, response_schema: dict, response: dict) -> bool:
        """
        스키마를 체크합니다.
        :return:
        """
        try:
            validate(instance=response, schema=response_schema)
            return True
        except Exception as e:
            print("실패")
            BaseTest.logger.info(e)
            return False


    def is_status_code_between_200_and_300_and_response_time_is_not_slowed(self, response: requests.Response)->bool:
        """
        상태코드가 200에서 300사이 (정상범위) 면서 응답시간이 느리지 않은 경우를 체크합니다.
        :param response:
        :return: bool
        """

        return response.status_code >= 200 and response.status_code < 300 and response.elapsed.total_seconds() < 1.0

    def is_status_code_between_400_and_500_and_response_time_is_not_slowed(self, response:requests.Response)->bool:
        """
        상태코드가 400에서 500사이이면서 응답시간이 느리지 않은 경우를 체크합니다.
        :param response:
        :return: bool
        """

        return response.status_code >= 400 and response.status_code < 500 and response.elapsed.total_seconds() <1.0
