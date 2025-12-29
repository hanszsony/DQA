__API_VERSION = 1

import logging

import sys
from colorama import init, Fore, Style

from datetime import datetime


class ErrorInLogger(Exception):
    def __init__(self, message):
        self.message = message


# warn() 方法： 在早期版本的 Python 中，warn() 方法用于记录警告级别的日志消息。然而，自从 Python 2.6 版本开始，warn() 方法已经被废弃，并建议使用 warning() 方法代替。尽管 warn() 方法在大多数情况下仍然可用，但它在未来的 Python 版本中可能会被移除。
# warning() 方法： warning() 方法用于记录警告级别的日志消息，它是 logger 模块的一个方法。与 warn() 方法相比，warning() 方法更加标准化和推荐，因此在编写新代码时应该优先选择使用 warning() 方法来记录警告级别的日志消息。


class GlobalLogger(logging.Logger):
    def error(self, msg, *args, **kwargs):
        colored_msg = Fore.RED + str(msg) + Style.RESET_ALL
        super().error(colored_msg, *args, **kwargs)
        sys.exit(0)

    def warning(self, msg, *args, **kwargs):
        colored_msg = Fore.YELLOW + str(msg) + Style.RESET_ALL
        super().warning(colored_msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        colored_msg = Fore.GREEN + str(msg) + Style.RESET_ALL
        super().info(colored_msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        colored_msg = Fore.WHITE + str(msg) + Style.RESET_ALL
        super().debug(colored_msg, *args, **kwargs)


ENCODE = "UTF-8"
FORMAT_FILE_TIME = r"%Y-%m-%d_%H-%M"

FORMATTER = logging.Formatter("%(asctime)s - %(funcName)s - %(message)s")


def __get_log_file_name(folder: str) -> str:
    import mpath

    current_timestamp = int(datetime.now().timestamp())
    current_time = datetime.fromtimestamp(current_timestamp).strftime(FORMAT_FILE_TIME)
    return mpath.join_file_path(folder, f"{current_time}.log")


def __setup_handler_file(log_folder: str, level: int) -> logging.FileHandler:
    """设置文件处理器"""
    file_logger = __get_log_file_name(log_folder)
    handler = logging.FileHandler(file_logger, encoding=ENCODE)
    handler.setLevel(level)
    handler.setFormatter(FORMATTER)
    return handler


def __setup_handler_console(level: int) -> logging.StreamHandler:
    """设置控制台处理器"""
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(FORMATTER)
    return handler


def setup_logger_console_debug():
    # init colorama
    init()
    logger = GlobalLogger(__name__)
    logger.setLevel(logging.NOTSET)
    console_handler = __setup_handler_console(logging.DEBUG)
    logger.addHandler(console_handler)
    return logger


def reload_logger_file_debug_console_info(
    logger: GlobalLogger, log_folder: str
) -> GlobalLogger:
    """重新加载文件日志处理器，设置为调试级别，并添加控制台输出信息级别日志"""
    # logger.handlers.clear()  # 移除所有处理器
    file_handler = __setup_handler_file(log_folder, logging.DEBUG)
    logger.addHandler(file_handler)

    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):  # 找到控制台输出的 handler
            handler.setLevel(logging.INFO)
            break
    # console_handler = __setup_handler_console()
    # logger.addHandler(console_handler)

    return logger


def reload_logger_file_debug_console_debug(
    logger: GlobalLogger, log_folder: str
) -> GlobalLogger:
    """重新加载文件日志处理器，设置为调试级别，并添加控制台输出调试级别日志"""
    # logger.handlers.clear()  # 移除所有处理器
    file_handler = __setup_handler_file(log_folder, logging.DEBUG)
    logger.addHandler(file_handler)

    # console_handler = __setup_handler_console(logging.DEBUG)
    # logger.addHandler(console_handler)

    return logger


if logging.getLogger(__name__).hasHandlers():
    LOGGER = logging.getLogger(__name__)
else:
    LOGGER = setup_logger_console_debug()
