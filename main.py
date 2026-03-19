# from networksecurity.components.data_ingestion import DataIngestion
# from networksecurity.components.data_validation import DataValidation
# from networksecurity.components.data_transformation import DataTransformation
# from networksecurity.components.model_trainer import ModelTrainer
# from networksecurity.exception.exception import NetworkSecurityException
# from networksecurity.logging.logger import logging
# from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig, DataTransformationConfig, ModelTrainerConfig
# from networksecurity.entity.config_entity import TrainingPipelineConfig

 

# import sys

# if __name__=='__main__':
#     try:
#         trainingpipelineconfig=TrainingPipelineConfig()
#         dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
#         data_ingestion=DataIngestion(dataingestionconfig)
#         logging.info("Initiate the data ingestion")
#         dataingestionartifact=data_ingestion.initiate_data_ingestion()
#         logging.info("Data Initiation Completed")
#         print(dataingestionartifact)
#         data_validation_config=DataValidationConfig(trainingpipelineconfig)
#         data_validation=DataValidation(dataingestionartifact,data_validation_config)
#         logging.info("Initiate the data Validation")
#         data_validation_artifact=data_validation.initiate_data_validation()
#         logging.info("data Validation Completed")
#         print(data_validation_artifact)

#         data_transformation_config = DataTransformationConfig(trainingpipelineconfig)
#         logging.info("Data Transformation Started")
#         data_transformation = DataTransformation(data_validation_artifact,data_transformation_config)
#         data_transformation_artifact = data_transformation.initiate_data_transformation()
#         print(data_transformation_artifact)
#         logging.info("Data Transformation Completed")


#         logging.info("Model Training stared")
#         model_trainer_config=ModelTrainerConfig(trainingpipelineconfig)
#         model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
#         model_trainer_artifact=model_trainer.initiate_model_trainer()

#         logging.info("Model Training artifact created")

#     except Exception as e:
#            raise NetworkSecurityException(e,sys) from e


# main.py

import sys

# Import all necessary components and entities
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
# NEW: Import ModelEvaluation and ModelPusher
from networksecurity.components.model_evaluation import ModelEvaluation
from networksecurity.components.model_pusher import ModelPusher
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    # NEW: Import ModelEvaluationConfig and ModelPusherConfig
    ModelEvaluationConfig,
    ModelPusherConfig,
    TrainingPipelineConfig
)

if __name__ == '__main__':
    try:
        # Initialize the training pipeline configuration
        trainingpipelineconfig = TrainingPipelineConfig()
        
        # --- Data Ingestion Stage ---
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion Completed")
        print(f"Data Ingestion Artifact: {dataingestionartifact}")
        
        # --- Data Validation Stage ---
        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(dataingestionartifact, data_validation_config)
        logging.info("Initiate the data Validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation Completed")
        print(f"Data Validation Artifact: {data_validation_artifact}")

        # --- Data Transformation Stage ---
        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)
        logging.info("Data Transformation Started")
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data Transformation Completed")
        print(f"Data Transformation Artifact: {data_transformation_artifact}")

        # --- Model Training Stage ---
        logging.info("Model Training started")
        model_trainer_config = ModelTrainerConfig(trainingpipelineconfig)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info("Model Training completed")
        print(f"Model Trainer Artifact: {model_trainer_artifact}")
        
        # --- Model Evaluation Stage ---
        logging.info("Model Evaluation started")
        model_evaluation_config = ModelEvaluationConfig(trainingpipelineconfig)
        model_evaluation = ModelEvaluation(data_validation_artifact=data_validation_artifact, 
                                            data_transformation_artifact=data_transformation_artifact, 
                                            model_trainer_artifact=model_trainer_artifact,
                                            model_evaluation_config=model_evaluation_config)
        # Evaluate the trained model using validation and transformation artifacts; 
        # the artifact contains evaluation metrics and model comparison results.
        model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
        logging.info("Model Evaluation completed")
        print(f"Model Evaluation Artifact: {model_evaluation_artifact}")

        # --- Model Pusher Stage ---
        logging.info("Model Pusher started")
        model_pusher_config = ModelPusherConfig(trainingpipelineconfig)
        model_pusher = ModelPusher(data_transformation_artifact=data_transformation_artifact, 
                                    model_trainer_artifact=model_trainer_artifact, 
                                    model_pusher_config=model_pusher_config)
        model_pusher_artifact = model_pusher.initiate_model_pusher()
        logging.info("Model Pusher completed")
        print(f"Model Pusher Artifact: {model_pusher_artifact}")


    except Exception as e:
        # Properly handle and re-raise exceptions for a clean traceback
        raise NetworkSecurityException(e, sys) from e
