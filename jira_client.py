from datetime import datetime
from enum import Enum
from helper import get_jira_env, get_current_datetime

import requests
from requests.auth import HTTPBasicAuth


class JIRAIssueType(Enum):
    TASK = "10001"
    EPIC = "10002"
    BUG = "10005"


class JIRAIssueLinkType(Enum):
    BLOCK = {
        "id": "10000",
        "name": "Blocks",
        "inward": "is blocked by",
        "outward": "blocks",
    }
    CLONERS = {
        "id": "10001",
        "name": "Cloners",
        "inward": "is cloned by",
        "outward": "clones",
    }
    RELATES = {
        "id": "10003",
        "name": "Relates",
        "inward": "relates to",
        "outward": "relates to",
    }


class JIRAClient:
    """
    지라 API 를 조작하기 위한 클라이언트
    """

    def __init__(self):
        self.base_url = "https://dhpractice.atlassian.net"
        self.create_issue_resource = "/rest/api/2/issue"
        self.project_key = "KAN"
        self.project_id = "10000"
        self.api_key = get_jira_env("JIRA_API_KEY")
        self.user_name = get_jira_env("USER_NAME")
        self.account_id = get_jira_env("ACCOUNT_ID")
        self.basic_auth = HTTPBasicAuth(self.user_name, self.api_key)
        self.create_issue_data = {
            "fields": {
                "assignee": {
                    "id": ''
                },
                "description": "",
                "issuetype": {
                    "id": ''
                },
                "labels": [
                    "createAPI"
                ],
                "project": {
                    "id": self.project_id
                },
                "reporter": {
                    "id": self.account_id
                },
                "summary": ''
            }
        }

    def create_task_ticket(self):
        """
        Task ticket을 생성합니다.
        이것은 버그 이슈들을 묶기 위한 트래킹용 티켓입니다.

        """
        now = datetime.now()

        data = self.create_issue_data.copy()
        data['fields']['assignee']['id'] = self.account_id
        data['fields']['description'] = "테스트 실행 후 발생한 이슈 묶음용 티켓"
        data['fields']['issuetype']['id'] = JIRAIssueType.TASK.value
        data['fields']['summary'] = f"{now.strftime('%y-%m-%d %H:%M')} 자동 테스트 실행 후 이슈 묶음용 티켓"

        response = requests.post(auth=self.basic_auth, url=f"{self.base_url}{self.create_issue_resource}", json=data)
        return response.json()['key']

    def create_bug_ticket_when_test_failed(self, ticket_key: str, test_name: str, traceback: str,
                                           exception_location: str):
        """
        테스트를 실행했을 때 버그티켓을 설정합니다.
        이때 묶음용 티켓의 키값을 전달받습니다.

        """
        description_text = f"""
        ```text
        {traceback}\n
        ```
        Exception location : {exception_location}
        
        """
        data = self.create_issue_data.copy()
        data['fields']['assignee']['id'] = self.account_id
        data['fields']['description'] = description_text
        data['fields']['issuetype']['id'] = JIRAIssueType.BUG.value
        data['fields']['summary'] = f"{test_name}"
        data['fields']['labels'].append("AutomationAPITest")
        data["update"] = {
            "issuelinks": [
                {
                    "add": {
                        "type": {
                            "name": JIRAIssueLinkType.RELATES.value["name"],
                            "inward": JIRAIssueLinkType.RELATES.value['inward'],
                            "outward": JIRAIssueLinkType.RELATES.value['outward']
                        },
                        "outwardIssue": {
                            "key": ticket_key
                        }
                    }
                }
            ]
        }

        requests.post(auth=self.basic_auth, url=f"{self.base_url}{self.create_issue_resource}", json=data)
