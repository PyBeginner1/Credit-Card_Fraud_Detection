import os,sys
import yaml
import dill

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


def save_object(file_path:str,obj):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)
    except Exception as e:
        logging.info(e)
        raise FraudException(e,sys) from e 


