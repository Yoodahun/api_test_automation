import logging
import os.path
from datetime import datetime


def get_logger(execute_point_name: str) -> logging.Logger:
    """
    logger의 셋팅을 담당합니다. 마지막에는 로거를 리턴합니다.
    파라미터로는 로깅 객체를 호출하는 클래스의 이름이 넘어갑니다.

    :return: Logger
    """
    logger = logging.getLogger(execute_point_name)
    logger.setLevel(logging.DEBUG)

    return logger


def get_jira_env(key:str)->str:
    """
    JIRA 설정 파일 값을 읽어옵니다.
    :param key:
    :return:
    """
    current_file_path = os.path.abspath(__file__)
    project_root_path = os.path.dirname(current_file_path)
    jira_api_key_file_path = os.path.join(project_root_path, "resources", "jira_api_key.py")

    if os.path.exists(jira_api_key_file_path):
        from resources.jira_api_key import info
        return info[key]
    else:
        return os.environ.get(key)


def get_current_datetime() -> str:
    """
    현재 날짜와 시간을 'YY-MM-DD HH:MM' 형식의 문자열로 반환합니다.
    :return: 포맷된 날짜와 시간 문자열
    """
    # 현재 날짜와 시간을 가져옵니다
    now = datetime.now()

    # 날짜와 시간을 'YY-MM-DD HH:MM' 형식으로 포맷합니다
    formatted_date_time = now.strftime('%y-%m-%d %H:%M')

    return formatted_date_time
