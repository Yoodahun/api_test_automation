# api_test_automation using JIRA API
포트폴리오 용도로 만든 API Test 프로젝트 입니다.

호출 API는 아래 API를 사용하였습니다.

- https://reqres.in/

본 프로젝트에서는 **API의 호출 리소스별로 클래스를 만들어 테스트 코드를 좀 더 가볍고 적은 코드로 읽을 수 있게끔 시도** 하였습니다.


---

## Directory structure
```text
├── README.md
├── conftest.py
├── helper.py
├── jira_client.py
├── pytest.ini
├── requirements.txt
├── resources
│   └── jira_api_key.py
├── src
│   ├── base_api_client.py
│   └── resource
│       ├── __init__.py
│       ├── register.py
│       └── user.py
└── test
    ├── base_test.py
    ├── test_register.py
    └── test_user.py

```

### src
`src` 폴더 하위에는 API호출에 필요한 기본적인 것들을 담아놓은 `base_api_client`가 있고, 그 아래에 api의 resource별로 클래스를 만들었습니다. 모든 api리소스들은 `BaseAPIClient` 를 상속받아 api호출에 필요한 기반 액션들에 대해 재사용하여 사용할 수 있도록 하였습니다.

### test
`test` 폴더 하위에는 각각의 API 리소스 별로 테스트 파일을 생성해놓았으며, 테스트도 마찬가지로 자주 사용하는 `assert` 행위들을 한데 모은 `base_test` 를 생성해놓고, 하위 테스트 클래스들에서 `BaseTest` 를 상속받도록 하였습니다.

### conftest.py
pytest에서 실행에 필요한 fixture 및 hook을 정의해놓았습니다.

### helper.py
유틸리티 성격을 가진 모듈들을 넣어놓았습니다.

### jira_client.py
커맨드 실행 시에 `--report_to_jira` 를 입력하게 된다면 `resources/jira_api_key.py` 가 존재하거나 환경설정 파일에 원하는 키값이 존재한다면 에러가 발생했을 때 이슈를 JIRA로 리포트 하도록 되어있습니다.

해당 파일에는 그런 리포트에 필요한 동작들을 모아놓았습니다.

---

## Testing
테스트는 간단한 내용만 작성해놓았습니다.

### test_register
- ID 1개 등록하기
- ID 등록에 실패하기

### test_user
- 전체 유저 호출하기
- 유저 1명 호출 후 JSON 스키마 검증하기
- 존재하지 않는 임의의 유저 호출하기
- 유저 1명 생성하기
- 유저 1명 생성 후 해당 유저 조회하기
- 유저 1명 삭제하기
- 유저 1명 호출에 실패하기 _(테스트 실패가 아닌 의도적인 실패 발생)_

각각의 테스트 내용에 대해서는 테스트코드를 직접 확인해주시면 감사하겠습니다.

---

## Reporting

본 프로젝트에서 리포트는 JIRA로 수행합니다.
지라로 리포트하기 위한 전제조건은 아래와 같습니다.

- `jira_api_key.py` 내에 아래의 키 값들이 존재할 것.
  - JIRA_API_KEY
  - USER_NAME
  - ACCOUNT_ID

API KEY같은 경우에는 민감한 정보이므로 `jira_api_key.py` 는 `.gitignore` 에 등록되어있으며 로컬에서 실행할 때는 이 폴더를 만들어 값을 적절하게 기재해주시거나 환경설정파일에 설정을 해주어야합니다.

JIRA로의 리포트가 실행될 때에는 전체 테스트 실행 전에 묶음용 티켓이 한 번 생성되고, 그 이후 각각의 테스트가 실패할 때마다 버그티켓을 생성하고, 전체 테스트 실행 시 최초 생성했던 묶음용 티켓과 **relates** 관계로 링크가 설정됩니다.

리포트 로직에 대해서는 `conftest.py` 내에서 아래 fixture와 hook을 참고해주세요.
- `setup_jira_ticket()`
- `pytest_runtest_makereport()`

---
