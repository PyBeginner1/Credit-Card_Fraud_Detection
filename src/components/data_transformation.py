import os, sys
import pandas as pd

from sklearn.preprocessing import StandardScaler

from src.logger import logging
from src.exception import FraudException
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact
from src.util.util import save_object

class DataTransformation:
    def __init__(self, data_transformation_config: DataTransformationConfig, data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise FraudException(e,sys) from e
        

    def extract_necessary_and_drop_unncessary_columns(self, data):
        try:
            data['TX_DATETIME']=pd.to_datetime(data['TX_DATETIME'])
            data['day'] = data['TX_DATETIME'].dt.day
            data['month'] = data['TX_DATETIME'].dt.month

            drop_columns = ['Unnamed: 0', 'TX_FRAUD_SCENARIO','TX_DATETIME']
            data.drop(drop_columns, axis = 1, inplace = True)

            return data
        except Exception as e:
            raise FraudException(e,sys) from e
        
    
    def initiate_data_transformation(self):
        try:
            logging.info('Obtaining train and test data')
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_df = pd.read_csv(train_file_path)
            test_df = pd.read_csv(test_file_path)

            logging.info('Extracting datetime and removing unnecessary columns')
            new_train_df = self.extract_necessary_and_drop_unncessary_columns(data=train_df)
            new_test_df = self.extract_necessary_and_drop_unncessary_columns(data=test_df)

            logging.info('Obtaining preprocessing objects')
            scaler = StandardScaler()

            target = 'TX_FRAUD'

            input_train_df = new_train_df.drop(target, axis = 1)
            target_train = new_train_df[target]

            input_test_df = new_test_df.drop(target, axis= 1)
            target_test = new_test_df[target]

            columns = input_train_df.columns

            logging.info(f"Applying preprocessing object on training dataframe and testing dataframe")
            new_scaled_train = pd.DataFrame(scaler.fit_transform(input_train_df), columns = columns)
            new_scaled_test = pd.DataFrame(scaler.transform(input_test_df), columns = columns)

            new_scaled_train[target] = target_train
            new_scaled_test[target] = target_test

            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir

            train_file_name = os.path.basename(train_file_path)
            test_file_name = os.path.basename(test_file_path)

            transformed_train_file_path = os.path.join(transformed_train_dir, train_file_name)
            transformed_test_file_path = os.path.join(transformed_test_dir, test_file_name)

            logging.info(f"Saving transformed training and testing array.")

            os.makedirs(os.path.dirname(transformed_train_file_path), exist_ok = True)
            os.makedirs(os.path.dirname(transformed_test_file_path), exist_ok = True)

            new_scaled_train.to_csv(transformed_train_file_path, index = False)
            new_scaled_test.to_csv(transformed_test_file_path, index = False)

            preprocessing_object_file_path = self.data_transformation_config.preprocessed_object_file_path

            logging.info(f"Saving preprocessing object.")
            save_object(file_path = preprocessing_object_file_path, obj = scaler)

            data_transformation_artifact = DataTransformationArtifact(
                                                        is_transformed = True,
                                                        message = 'Data Transformation successfull',
                                                        transformed_train_file_path = transformed_train_file_path,
                                                        transformed_test_file_path = transformed_test_file_path,
                                                        preprocessed_object_file_path = preprocessing_object_file_path
                                                            )

            logging.info(f'Data Transformation Artifact: [{data_transformation_artifact}]')
            return data_transformation_artifact
        except Exception as e:
            raise e
    
    def __del__(self):
        logging.info(f"{'>>'*30}Data Transformation log completed.{'<<'*30} \n\n")

    