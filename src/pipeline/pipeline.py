import os, sys
from collections import namedtuple
from datetime import datetime

from src.logger import logging
from src.exception import FraudException
from src.config.configuration import ConfigurationManager
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation

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
        

    def start_data_transformation(self,data_ingestion_artifact: DataIngestionArtifact) -> DataTransformationArtifact:
        try:
            logging.info('Data Transformation Initiated')
            data_transformation = DataTransformation(data_transformation_config=self.config.get_data_transformation_config(),
                                                     data_ingestion_artifact=data_ingestion_artifact)
            return data_transformation.initiate_data_transformation()
        except Exception as e:
            raise FraudException(e,sys) from e


    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact)
            print(data_transformation_artifact)
        except Exception as e:
            raise FraudException(e,sys) from e