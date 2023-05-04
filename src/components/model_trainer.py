import os, sys
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split

from src.logger import logging
from src.exception import FraudException
from src.entity.artifact_entity import DataTransformationArtifact
from src.entity.config_entity import ModelTrainerConfig
from src.entity.model_factory import *
from src.util.util import load_object, save_object
from src.entity.artifact_entity import ModelTrainerArtifact

class FraudEstimatorModel:
    def __init__(self, preprocessing_object, trained_model_object):
        """
        TrainedModel constructor
        preprocessing_object: preprocessing_object
        trained_model_object: trained_model_object
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, X):
        """
        function accepts raw inputs and then transformed raw input using preprocessing_object
        which gurantees that the inputs are in the same format as the training data
        At last it perform prediction on transformed features
        """
        transformed_feature = self.preprocessing_object.transform(X)
        return self.trained_model_object.predict(transformed_feature)

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"

class ModelTrainer:
    def __init__(self, 
                 data_transformation_artifact: DataTransformationArtifact, 
                 model_trainer_config: ModelTrainerConfig):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise FraudException(e, sys) from e
        

    def initiate_model_trainer(self):
        try:
            logging.info('Loading Transformed Train dataset')
            transformed_train_data_file_path = self.data_transformation_artifact.transformed_train_file_path
            train = pd.read_csv(transformed_train_data_file_path)

            logging.info('Loading Transformed Test dataset')
            transformed_test_data_file_path = self.data_transformation_artifact.transformed_test_file_path
            test = pd.read_csv(transformed_test_data_file_path)

            logging.info('Splitting the dataset into features and target')
            X_train = train.drop('TX_FRAUD', axis = 1)
            y_train = train['TX_FRAUD']
            X_test = test.drop('TX_FRAUD', axis = 1)
            y_test = test['TX_FRAUD']

            #X_train, y_train, X_test, y_test = train.iloc[:,:-1], train.iloc[:,-1], test.iloc[:,:-1], test.iloc[:,-1]

            logging.info(f"Extracting model config file path")
            model_config_file_path = self.model_trainer_config.model_config_file_path

            logging.info(f"Initializing model factory class using above model config file: {model_config_file_path}")
            model_factory=ModelFactory(model_config_path=model_config_file_path)

            base_accuracy=self.model_trainer_config.base_accuracy
            logging.info(f"Expected accuracy: {base_accuracy}")

            logging.info(f"Initiating operation model selecttion")
            best_model=model_factory.get_best_model(X=X_train,y=y_train,base_accuracy=base_accuracy)

            logging.info(f"Best model found on training dataset: {best_model}")

            logging.info(f"Extracting trained model list.")
            grid_searched_best_model_list:List[GridSearchedBestModel]=model_factory.grid_searched_best_model_list

            model_list = [model.best_model for model in grid_searched_best_model_list ]
            logging.info(f"Evaluation all trained model on training and testing dataset both")
            metric_info:MetricInfoArtifact = evaluate_regression_model(model_list=model_list,X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,base_accuracy=base_accuracy)

            preprocessing_obj=load_object(file_path=self.data_transformation_artifact.preprocessed_object_file_path)
            model_object = metric_info.model_object

            trained_model_file_path=self.model_trainer_config.trained_model_file_path
            housing_model = FraudEstimatorModel(preprocessing_object=preprocessing_obj,trained_model_object=model_object)
            logging.info(f"Saving model at path: {trained_model_file_path}")
            save_object(file_path=trained_model_file_path,obj=housing_model)

            model_trainer_artifact=  ModelTrainerArtifact(is_trained=True,message="Model Trained successfully",
            trained_model_file_path=trained_model_file_path,
            train_accuracy=metric_info.train_accuracy,
            test_accuracy=metric_info.test_accuracy,
            model_accuracy=metric_info.model_accuracy
            
            )

            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise FraudException(e, sys) from e