import os,sys

from src.logger import logging
from src.exception import FraudException
from src.constant import *
from src.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataTransformationConfig, ModelTrainerConfig
from src.util.util import read_yaml_file

class ConfigurationManager:
    def __init__(self, config_file_path=CONFIG_FILE_PATH, current_time_stamp:str = CURRENT_TIME_STAMP):
        self.config = read_yaml_file(config_file_path)
        self.time_stamp = current_time_stamp
        self.training_pipeline_config = self.get_training_pipeline_config()

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            logging.info('Config for Data Ingestion started')
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_ingestion_artifact_dir = os.path.join(artifact_dir, DATA_INGESTION_ARTIFACT_DIR, self.time_stamp)

            data_ingestion_config_info = self.config[DATA_INGESTION_CONFIG_KEY]

            ingested_train_dir = os.path.join(data_ingestion_artifact_dir, data_ingestion_config_info[DATA_INGESTION_TRAIN_DIR_KEY])

            ingested_test_dir = os.path.join(data_ingestion_artifact_dir, data_ingestion_config_info[DATA_INGESTION_TEST_DIR_KEY])

            data_ingestion_config = DataIngestionConfig(
                ingested_train_dir = ingested_train_dir,
                ingested_test_dir = ingested_test_dir
            )
            logging.info(f"Data Ingestion config: [{data_ingestion_config}]")
            return data_ingestion_config
        except Exception as e:
            raise FraudException(e, sys) from e
        

    def get_data_transformation_config(self) -> DataTransformationConfig:
        try:
            logging.info('Config for Data Transformation started')
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_transformation_artifact_dir = os.path.join(artifact_dir, DATA_TRANSFORMATION_ARTIFACT_DIR, self.time_stamp)

            data_transformation_config_info = self.config[DATA_TRANSFORMATION_CONFIG_KEY]

            transformed_train_dir = os.path.join(data_transformation_artifact_dir,
                                                 data_transformation_config_info[DATA_TRANSFORMATION_DIR_NAME_KEY],
                                                 data_transformation_config_info[DATA_TRANSFORMATION_TRAIN_DIR_NAME_KEY])
            
            transformed_test_dir = os.path.join(data_transformation_artifact_dir,
                                                data_transformation_config_info[DATA_TRANSFORMATION_DIR_NAME_KEY],
                                                data_transformation_config_info[DATA_TRANSFORMATION_TEST_DIR_NAME_KEY])
            
            preprocessed_object_file_path = os.path.join(data_transformation_artifact_dir,
                                                         data_transformation_config_info[DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY],
                                                         data_transformation_config_info[DATA_TRANSFORMATION_PREPROCESSED_FILE_NAME_KEY])

            data_transformation_config = DataTransformationConfig(
                                            transformed_train_dir=transformed_train_dir,
                                            transformed_test_dir=transformed_test_dir,
                                            preprocessed_object_file_path=preprocessed_object_file_path
                                            )
            logging.info(f"Data Transformation Config: {data_transformation_config}")
            return data_transformation_config
        except Exception as e:
            raise FraudException(e, sys) from e
        

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        try:
            logging.info('Config for Model trainer started')

            artifact_dir = self.training_pipeline_config.artifact_dir
            model_trainer_artifact_dir = os.path.join(artifact_dir, MODEL_TRAINER_ARTIFACT_DIR, 
                                                      self.time_stamp)
            
            model_trainer_config_info = self.config[MODEL_TRAINER_CONFIG_KEY]

            trained_model_file_path = os.path.join(model_trainer_artifact_dir, 
                                                   model_trainer_config_info[MODEL_TRAINER_TRAINED_MODEL_DIR_KEY],
                                                   model_trainer_config_info[MODEL_TRAINER_TRAINED_MODEL_FILE_NAME_KEY])
            
            base_accuracy = model_trainer_config_info[MODEL_TRAINER_BASE_ACCURACY_KEY]

            model_config_file_path = os.path.join(ROOT_DIR,
                                                  model_trainer_config_info[MODEL_TRAINER_MODEL_CONFIG_DIR_KEY],
                                                  model_trainer_config_info[MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY])

            model_trainer_config = ModelTrainerConfig(
                                                    trained_model_file_path=trained_model_file_path,
                                                    base_accuracy=base_accuracy,
                                                    model_config_file_path=model_config_file_path
                                                    )
            
            logging.info(f"Model Trainer Config: [{model_trainer_config}]")
            return model_trainer_config
        except Exception as e:
            raise FraudException(e, sys) from e


    def get_training_pipeline_config(self)->TrainingPipelineConfig:
        try:
            logging.info('Training pipeline config started')
            training_pipeline_config_info = self.config[TRAINING_PIPELINE_CONFIG_KEY]

            artifact_dir = os.path.join(ROOT_DIR, training_pipeline_config_info[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])

            training_pipeline_config = TrainingPipelineConfig(artifact_dir = artifact_dir)

            logging.info(f"Training pipeline config: [{training_pipeline_config}]")
            return training_pipeline_config
        except Exception as e:
            raise FraudException(e,sys) from e