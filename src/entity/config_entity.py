
from collections import namedtuple


TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", ["artifact_dir"])


DataIngestionConfig = namedtuple('DataIngestionConfig',
                                ['ingested_train_dir','ingested_test_dir'])