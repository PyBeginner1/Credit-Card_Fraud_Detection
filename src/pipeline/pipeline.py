import os, sys
from collections import namedtuple
from datetime import datetime

from src.logger import logging
from src.exception import FraudException
from src.config.configuration import ConfigurationManager
from src.entity.artifact_entity import DataIngestionArtifact
from src.components.data_ingestion import DataIngestion

class Pipeline:
    def __init__(self, config : ConfigurationManager):
        try:
            os.makedirs(config.get_training_pipeline_config().artifact_dir, exist_ok = True)
            self.config = config
        except Exception as e:
            raise FraudException(e, sys) from e


    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise FraudException(e,sys) from e


    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            print(data_ingestion_artifact)
        except Exception as e:
            raise FraudException(e,sys) from e