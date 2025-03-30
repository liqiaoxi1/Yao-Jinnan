"""
    general logger
"""
import logging
import logging.handlers
class Logger:
    """
        logger class
    """
    __logger = None

    @classmethod
    def __get_logger(cls):
        if cls.__logger is None:
            cls.__logger = logging.getLogger("main")
            cls.__logger.setLevel(level=logging.DEBUG)

            formatter = logging.Formatter(
                '[%(asctime)s][%(threadName)s][%(levelname)s] %(message)s')

            handler = logging.handlers.TimedRotatingFileHandler(
                "fastapi.log", when='D', interval=1, backupCount=0)
            handler.suffix = '%Y-%m-%d.log'
            handler.setLevel(logging.INFO)
            handler.setFormatter(formatter)

            console = logging.StreamHandler()
            console.setFormatter(formatter)
            console.setLevel(logging.DEBUG)

            cls.__logger.addHandler(handler)
            cls.__logger.addHandler(console)

        return cls.__logger

    @classmethod
    def error(cls, message):
        """
            log error
        """
        cls.__get_logger().error(message)

    @classmethod
    def info(cls, message):
        """
            log information
        """
        cls.__get_logger().info(message)

    @classmethod
    def warning(cls, message):
        """
            log warning
        """
        cls.__get_logger().warning(message)

    @classmethod
    def debug(cls, message):
        """
            log debug informtion
        """
        cls.__get_logger().debug(message)

    @classmethod
    def exception(cls, message):
        """
            log exception 
        """
        cls.__get_logger().exception(message)
