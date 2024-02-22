import inspect
import logging


class BaseClass:
    def get_logger(self):
        # captures the file name at the runtime
        logger_name = inspect.stack()[1][3]
        logger = logging.getLogger(logger_name)
        file_handler = logging.FileHandler('login_test.log')
        formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(name)s : %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        # print log statement info and following
        logger.setLevel(logging.INFO)
        # logger.debug("A debug statement is executed")
        # logger.info("Information statement")
        # logger.warning("Something is in warning mode")
        # logger.error("A major error has happened")
        # logger.critical("Critical issue")
        return logger
