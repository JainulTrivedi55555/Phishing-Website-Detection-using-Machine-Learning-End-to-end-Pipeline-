# import sys
# import os
# import shutil

# from networksecurity.exception.exception import NetworkSecurityException
# from networksecurity.logging.logger import logging
# from networksecurity.pipeline.training_pipeline import TrainingPipeline

# from fastapi.middleware.cors import CORSMiddleware
# from fastapi import FastAPI, File, UploadFile, Request
# from uvicorn import run as app_run
# from fastapi.responses import Response
# from starlette.responses import RedirectResponse
# from pydantic import BaseModel

# class UserData(BaseModel):
#     user_input: str

# app = FastAPI()
# origins = ["*"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/", tags=["authentication"])
# async def index():
#     return RedirectResponse(url="/docs")

# @app.get("/train")
# async def train_route():
#     try:
#         logging.info("Starting training pipeline...")
#         train_pipeline = TrainingPipeline()
#         train_pipeline.run_pipeline()
#         logging.info("Training pipeline finished successfully.")
#         return Response("Training is successful")
#     except Exception as e:
#         logging.error(f"Error during training: {e}")
#         raise NetworkSecurityException(e, sys)

# # Placeholder for the predict route that requires python-multipart
# @app.post("/predict")
# async def predict_route(file: UploadFile = File(...)):
#     try:
#         logging.info(f"Received file for prediction: {file.filename}")

#         # The following is a placeholder for your actual prediction logic.
#         # It simply saves the file to a temporary location.
#         # You would replace this with your model's prediction logic.
#         temp_file_path = f"temp_{file.filename}"
#         with open(temp_file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)
            
#         # Example of where you would call your prediction function
#         # prediction_result = your_model.predict(temp_file_path)

#         logging.info(f"File saved successfully at {temp_file_path}")
#         return {"filename": file.filename, "message": "File processed successfully. Replace this with your prediction logic."}
#     except Exception as e:
#         logging.error(f"Error during prediction: {e}")
#         raise NetworkSecurityException(e, sys)

# if __name__ == "__main__":
#     app_run(app, host="0.0.0.0", port=8000)

import sys
import os
import shutil
import pandas as pd
import numpy as np
import pickle

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from pydantic import BaseModel

# Define the ROOT_DIR to resolve the NameError at the very beginning of the script
# This ensures that all file paths are correctly referenced from the project root.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))

class UserData(BaseModel):
    user_input: str

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        logging.info("Starting training pipeline...")
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        logging.info("Training pipeline finished successfully.")
        return Response("Training is successful")
    except Exception as e:
        logging.error(f"Error during training: {e}")
        raise NetworkSecurityException(e, sys)

@app.post("/predict")
async def predict_route(file: UploadFile = File(...)):
    try:
        logging.info(f"Received file for prediction: {file.filename}")

        # The paths below are critical. They must match the output paths from your training pipeline.
        artifacts_dir = os.path.join(ROOT_DIR, "networksecurity", "artifacts")
        trained_model_path = os.path.join(artifacts_dir, "model_trainer", "trained_model_object.pkl")
        preprocessor_path = os.path.join(artifacts_dir, "data_transformation", "preprocessor.pkl")

        # Check if model and preprocessor exist before attempting to load them
        if not os.path.exists(trained_model_path) or not os.path.exists(preprocessor_path):
            return Response("Model or preprocessor not found. Please run the training pipeline first.", status_code=404)

        # Load the trained model and preprocessor
        with open(trained_model_path, "rb") as f:
            model = pickle.load(f)
        
        with open(preprocessor_path, "rb") as f:
            preprocessor = pickle.load(f)

        # Read the uploaded file into a pandas DataFrame
        df = pd.read_csv(file.file)

        # Use the preprocessor to transform the data
        transformed_data = preprocessor.transform(df)

        # Make predictions using the loaded model
        predictions = model.predict(transformed_data)

        # Add predictions to the original DataFrame
        df["predicted_label"] = predictions

        # Create a directory for prediction output if it doesn't exist
        prediction_output_dir = os.path.join(artifacts_dir, "prediction_output")
        os.makedirs(prediction_output_dir, exist_ok=True)

        # Save the DataFrame with predictions to a new CSV file
        output_file_path = os.path.join(prediction_output_dir, "prediction_output.csv")
        df.to_csv(output_file_path, index=False)

        logging.info(f"Predictions saved to {output_file_path}")
        return Response(f"Prediction successful. Output saved to {output_file_path}")

    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8000)