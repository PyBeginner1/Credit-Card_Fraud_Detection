import os
from datetime import datetime

ROOT_DIR = os.getcwd()

CONFIG_DIR='config'
CONFIG_FILE='config.yaml'
SCHEMA_FILE='schema.yaml'

CONFIG_FILE_PATH=os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE)


def get_current_time_stamp():
    return f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

CURRENT_TIME_STAMP = get_current_time_stamp()
