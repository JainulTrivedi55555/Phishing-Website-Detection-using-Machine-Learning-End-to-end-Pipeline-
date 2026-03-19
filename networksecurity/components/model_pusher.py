# networksecurity/components/model_pusher.py

import sys
import shutil
import os

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import ModelPusherConfig
from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact,
    ModelPusherArtifact
)

# Placeholder ModelPusher class
class ModelPusher:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact,
                 model_trainer_artifact: ModelTrainerArtifact,
                 model_pusher_config: ModelPusherConfig):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_pusher_config = model_pusher_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        """
        This method will copy the trained model and preprocessor to a production directory.
        """
        try:
            logging.info("Starting model pusher process...")
            
            # Create the production directory if it doesn't exist
            os.makedirs(self.model_pusher_config.pushed_model_dir, exist_ok=True)
            
            # Copy the trained model
            source_model_path = self.model_trainer_artifact.trained_model_file_path
            destination_model_path = self.model_pusher_config.pushed_model_file_path
            shutil.copy(source_model_path, destination_model_path)
            logging.info(f"Copied trained model to production: {destination_model_path}")
            
            # Copy the preprocessor object
            source_preprocessor_path = self.data_transformation_artifact.transformed_object_file_path
            destination_preprocessor_path = os.path.join(
                self.model_pusher_config.pushed_model_dir, "preprocessor.pkl"
            )
            shutil.copy(source_preprocessor_path, destination_preprocessor_path)
            logging.info(f"Copied preprocessor to production: {destination_preprocessor_path}")
            
            model_pusher_artifact = ModelPusherArtifact(
                pushed_model_dir=self.model_pusher_config.pushed_model_dir,
                pushed_model_file_path=destination_model_path
            )
            
            logging.info("Model pusher completed.")
            return model_pusher_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
