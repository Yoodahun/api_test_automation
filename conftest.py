import pytest

from jira_client import JIRAClient
from src.resource.user import User

_ISSUE_TICKET_ID = ""
_JIRA_CLIENT = JIRAClient()


def pytest_addoption(parser):
    parser.addoption(
        "--report_to_jira",
        action="store_true",  # 이 옵션이 제공되면 값을 True로 저장
        default=False,  # 옵션이 없으면 기본값은 False
    )


@pytest.fixture(scope="session", autouse=True)
def setup_jira_ticket():
    # pass
    global _ISSUE_TICKET_ID
    _ISSUE_TICKET_ID = _JIRA_CLIENT.create_task_ticket()


@pytest.fixture(scope="function")
def create_a_user():
    """
    유저를 생성한 후 유저 아이디를 리턴합니다.
    :return: str
    """
    user_client = User()
    return user_client.create_a_user().json()["id"]

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # 테스트의 결과를 확인합니다
    report = yield
    result = report.get_result()
    if call.when == 'call':  # 실제 테스트 실행 후 결과를 처리
        if call.excinfo is not None:  # 예외가 발생했는지 확인
            outcome = call.excinfo.type.__name__  # 예외 유형
            if ('Error' in outcome) or ('Exception' in outcome):
                traceback_text = result.longreprtext

                # 실패 또는 에러가 발생했을 때의 조치

                _JIRA_CLIENT.create_bug_ticket_when_test_failed(
                    _ISSUE_TICKET_ID,
                    item.nodeid,
                    traceback_text,
                    str(item.location)
                )
