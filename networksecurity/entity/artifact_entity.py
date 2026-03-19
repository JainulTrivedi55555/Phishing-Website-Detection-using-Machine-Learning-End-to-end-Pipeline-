# from dataclasses import dataclass

# @dataclass
# class DataIngestionArtifact:
#     """
#     Data class for data ingestion artifact.
#     """
#     trained_file_path: str
#     test_file_path: str
    
# @dataclass
# class DataValidationArtifact:
#     validation_status:bool
#     valid_train_file_path:str
#     valid_test_file_path:str
#     invalid_train_file_path:str
#     invalid_test_file_path:str
#     drift_report_file_path:str

# @dataclass
# class DataTransformationArtifact:
#     transformed_object_file_path: str
#     transformed_train_file_path: str
#     transformed_test_file_path: str


# @dataclass
# class ClassificationMetricArtifact:
#     f1_score: float
#     precision_score: float
#     recall_score: float

# @dataclass
# class ModelTrainerArtifact:
#     trained_model_file_path: str
#     train_metric_artifact: ClassificationMetricArtifact
#     test_metric_artifact: ClassificationMetricArtifact


# networksecurity/entity/artifact_entity.py

# networksecurity/entity/artifact_entity.py

from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    """
    Data class for data ingestion artifact.
    """
    trained_file_path: str
    test_file_path: str
    
@dataclass
class DataValidationArtifact:
    validation_status:bool
    valid_train_file_path:str
    valid_test_file_path:str
    invalid_train_file_path:str
    invalid_test_file_path:str
    drift_report_file_path:str

@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str


@dataclass
class ClassificationMetricArtifact:
    f1_score: float
    precision_score: float
    recall_score: float

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    train_metric_artifact: ClassificationMetricArtifact
    test_metric_artifact: ClassificationMetricArtifact


# --- Corrected: Model Evaluation Artifact ---
# This class no longer has the 'pushed_model_file_path' argument.
@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool
    trained_model_file_path: str
    
# --- Corrected: Model Pusher Artifact ---
@dataclass
class ModelPusherArtifact:
    pushed_model_dir: str
    pushed_model_file_path: str
