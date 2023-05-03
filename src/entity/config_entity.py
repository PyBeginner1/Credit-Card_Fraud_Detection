
from collections import namedtuple


TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", ["artifact_dir"])


DataIngestionConfig = namedtuple('DataIngestionConfig',
                                ['ingested_train_dir','ingested_test_dir'])



DataTransformationConfig = namedtuple('DataTransformationConfig',
                                      [ "transformed_train_dir","transformed_test_dir","preprocessed_object_file_path"])


