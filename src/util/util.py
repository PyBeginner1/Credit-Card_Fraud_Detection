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
    


def load_object(file_path:str):
    """
    file_path: str
    """
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise FraudException(e,sys) from e
    

def write_yaml_file(file_path:str,data:dict=None):
    """
    Create yaml file 
    file_path: str
    data: dict
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path,"w") as yaml_file:
            if data is not None:
                yaml.dump(data,yaml_file)
    except Exception as e:
        raise FraudException(e,sys) from e
    

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


