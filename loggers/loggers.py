import inspect
import json
import logging
import logging.config
import os
from pathlib import Path


FOLDER_LOG = Path(Path(__file__).resolve().parent.parent.parent, 'logs')
LOGGING_CONFIG_FILE = Path(Path(__file__).resolve().parent, 'loggers.json')


def create_log_folder(folder: str = FOLDER_LOG) -> None:
    """Создать директорию с логами.

    Args:
        folder (str): Имя папки. Defaults to FOLDER_LOG.
    """
    if not os.path.exists(folder):
        os.mkdir(folder)


def get_logger(name: str, template: str = 'default') -> logging.Logger:
    """Получить логгер с заданным названием.

    Args:
        name (str): Имя.
        template (str): Шаблон. Defaults to 'default'.

    Returns:
        logging.Logger: объект логгера
    """
    with open(Path(LOGGING_CONFIG_FILE), 'r') as f_log_cfg:
        dict_config = json.load(f_log_cfg)
    create_log_folder()
    dict_config['handlers']['rotating_file']['filename'] = Path(FOLDER_LOG, dict_config['handlers']['rotating_file']['filename'])
    dict_config['loggers'][name] = dict_config['loggers'][template]
    logging.config.dictConfig(dict_config)
    return logging.getLogger(name)


def get_default_logger() -> logging.Logger:
    """Получить логгер по умолчанию.

    Returns:
        logging.Logger: объект логгера
    """
    # Подробно про логи
    # https://khashtamov.com/ru/python-logging/
    # https://habr.com/ru/companies/wunderfund/articles/683880/
    # https://python.readthedocs.io/en/stable/library/logging.html

    with open(Path(LOGGING_CONFIG_FILE), 'r') as f_log_cfg:
        dict_config = json.load(f_log_cfg)
    create_log_folder()
    dict_config['handlers']['rotating_file']['filename'] = Path(FOLDER_LOG, dict_config['handlers']['rotating_file']['filename'])
    logging.config.dictConfig(dict_config)
    return logging.getLogger('default')

