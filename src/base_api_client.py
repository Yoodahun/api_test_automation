import requests
import json
from helper import get_logger


class BaseAPIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.logger = get_logger(__name__)

    def get(self, endpoint:str, params=None, headers=None):
        """
        get 리퀘스트 호출
        :param endpoint:
        :param params:
        :param headers:
        :return:
        """
        self.logger.info("GET 실행")

        url = f"{self.base_url}/{self.__delete_first_slash_from_endpoint_string(endpoint)}"
        response = requests.get(url, params=params, headers=headers)
        return response

    def post(self, endpoint:str, data=None, headers=None):
        """
        post 리퀘스트 호출
        :param endpoint:
        :param data:
        :param headers:
        :return:
        """
        self.logger.info("POST 실행")
        url = f"{self.base_url}/{self.__delete_first_slash_from_endpoint_string(endpoint)}"
        response = requests.post(url, json=data, headers=headers)
        return response

    def put(self, endpoint:str, data=None, headers=None):
        """
        put 리퀘스트 호출
        :param endpoint:
        :param data:
        :param json:
        :param headers:
        :return:
        """
        url = f"{self.base_url}/{self.__delete_first_slash_from_endpoint_string(endpoint)}"
        response = requests.put(url, data=json.dumps(data), headers=headers)
        return response

    def delete(self, endpoint:str, headers=None):
        """
        delete 리퀘스트 호출
        :param endpoint:
        :param headers:
        :return:
        """
        url = f"{self.base_url}/{self.__delete_first_slash_from_endpoint_string(endpoint)}"
        response = requests.delete(url, headers=headers)
        return response


    def __delete_first_slash_from_endpoint_string(self, endpoint:str):
        """
        입력된 문자열에서 제일 첫자리에 슬래시 / 가 있다면 삭제한다.
        :param endpoint:
        :return:
        """
        return endpoint[1:] if endpoint.startswith('/') else endpoint