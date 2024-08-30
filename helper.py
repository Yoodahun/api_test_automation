import logging

def get_logger(execute_point_name: str) -> logging.Logger:
    """
    logger의 셋팅을 담당합니다. 마지막에는 로거를 리턴합니다.
    파라미터로는 로깅 객체를 호출하는 클래스의 이름이 넘어갑니다.

    :return: Logger
    """
    logger = logging.getLogger(execute_point_name)
    logger.setLevel(logging.DEBUG)

    return logger