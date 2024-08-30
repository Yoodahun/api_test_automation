import pytest

from src.resource.user import User




@pytest.fixture(scope="function")
def create_a_user():
    """
    유저를 생성한 후 유저 아이디를 리턴합니다.
    :return: str
    """
    user_client = User()
    return user_client.create_a_user().json()["id"]