from base_test import BaseTest

from src.resource.register import Register


class TestRegister(BaseTest):

    def setup_method(self):
        self.register = Register()

    def test_register_a_id(self):
        """
        아이디 하나를 등록합니다.
        등록 후 리턴되는 응답값의 스키마를 확인합니다.

        """
        response = self.register.register_id("eve.holt@reqres.in", "pistol")
        assert self.is_status_code_between_200_and_300_and_response_time_is_not_slowed(response)

        response_data = self.convert_json_data(response)
        assert self.validate_response_schema(self.register.schema_when_register_id, response_data)

    def test_fail_to_register_a_id(self):
        """
        아이디를 등록 시도합니다.
        패스워드를 없이 등록을 시도합니다.

        """
        response = self.register.register_id("eve.holt@reqres.in")
        assert self.is_status_code_between_200_and_300_and_response_time_is_not_slowed(response)