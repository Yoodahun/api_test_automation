from base_test import BaseTest
from src.resource.user import User


class TestUser(BaseTest):

    def setup_method(self):
        self.user = User()

    def test_get_user_list(self):
        """
        GET /api/users 에 대한 테스트 입니다.
        """
        response = self.user.get_list_users()
        assert self.is_status_code_between_200_and_300_and_response_time_is_not_slowed(response)

        response_data = self.convert_json_data(response)

        assert len(response_data["data"]) > 0
        assert "id" in response_data["data"][0]

    def test_user_schema(self):
        """
        GET /api/user/{user_id} 에 대한 테스트입니다.
        스키마도 체크도 같이 합니다.
        """
        response = self.user.get_single_user(user_id="2")
        assert self.is_status_code_between_200_and_300_and_response_time_is_not_slowed(response)

        response_data = self.convert_json_data(response)
        assert self.validate_response_schema(self.user.schema_when_get_single_user, response_data)

    def test_user_not_exist(self):
        """
        특정 유저가 존재하지 않는 경우에 대한 테스트입니다.

        """
        response = self.user.get_single_user(user_id="23")
        assert not self.is_status_code_between_200_and_300_and_response_time_is_not_slowed(response)
        assert self.is_status_code_between_400_and_500_and_response_time_is_not_slowed(response)
        response_data = self.convert_json_data(response)

        assert "data" not in response_data

    def test_create_a_user(self):
        """
        임의의 유저를 생성합니다.
        """
        response = self.user.create_a_user()
        assert self.is_status_code_between_200_and_300_and_response_time_is_not_slowed(response)

        response_data = self.convert_json_data(response)
        assert self.validate_response_schema(self.user.schema_when_user_created, response_data)

    def test_get_user_after_user_create(self, create_a_user):
        """
        유저를 fixture 로 생성한 후 아이디를 받아 해당 아이디로 조회합니다.
        호출하는 API는 실제 계정생성을 할 수는 없기 때문에 조회되지는 않습니다.
        """
        user_id = create_a_user

        response = self.user.get_single_user(user_id)
        assert self.is_status_code_between_200_and_300_and_response_time_is_not_slowed(response)

        response_data = self.convert_json_data(response)
        assert self.validate_response_schema(self.user.schema_when_get_single_user, response_data)

        # 생성한 아이디와 조회한 아이디가 일치하는지 확인한다.
        assert str(response_data["data"]["id"]) == user_id

    def test_delete_a_user(self):
        """
        임의의 유저를 삭제합니다.

        """
        response = self.user.delete_a_user("3")
        assert self.is_status_code_between_200_and_300_and_response_time_is_not_slowed(response)
        assert not self.is_status_code_between_400_and_500_and_response_time_is_not_slowed(response)


    def test_fail_get_single_user(self):
        """
        일부러 실패하는 테스트케이스입니다.

        """
        user_id = int("123@@!#13") # ValueError
        response = self.user.get_single_user(user_id)

        assert self.is_status_code_between_200_and_300_and_response_time_is_not_slowed(response)


