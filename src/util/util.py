import os,sys
import yaml


from src.logger import logging
from src.exception import FraudException


def read_yaml_file(file_path:str)->dict:
    """
    Reads yaml file and returns dictionary
    """
    try:
        with open(file_path,'r') as yaml_file:
            logging.info('Reading Yaml file')
            return yaml.safe_load(yaml_file)
    except Exception as e:
        logging.info(e)
        raise FraudException(e,sys) from e



