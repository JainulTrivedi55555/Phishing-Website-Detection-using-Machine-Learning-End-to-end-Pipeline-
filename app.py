import sys
import os
import re
from urllib.parse import urlparse

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
print(mongo_db_url)
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response, JSONResponse
from starlette.responses import RedirectResponse
from pydantic import BaseModel
import pandas as pd
import numpy as np
import pickle

from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")


class URLRequest(BaseModel):
    url: str


def extract_features_from_url(url: str, feature_columns: list) -> dict:
    """Extract phishing detection features from a raw URL string."""
    features = {}
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname or ""
        path = parsed.path or ""
        scheme = parsed.scheme or ""
        full_url = url
    except Exception:
        parsed = None
        hostname = ""
        path = ""
        scheme = ""
        full_url = url

    ip_pattern = re.compile(
        r"(([01]?\d\d?|2[0-4]\d|25[0-5])\.){3}([01]?\d\d?|2[0-4]\d|25[0-5])"
        r"|0x[0-9a-fA-F]{1,2}\.[0-9a-fA-F]{1,2}\.[0-9a-fA-F]{1,2}\.[0-9a-fA-F]{1,2}"
    )

    for col in feature_columns:
        if col == "having_IP_Address":
            features[col] = -1 if ip_pattern.search(full_url) else 1
        elif col == "URL_Length":
            features[col] = -1 if len(full_url) >= 75 else (0 if len(full_url) >= 54 else 1)
        elif col == "Shortining_Service":
            shorteners = ["bit.ly", "tinyurl", "goo.gl", "t.co", "ow.ly", "is.gd",
                          "buff.ly", "adf.ly", "tiny.cc", "short.to"]
            features[col] = -1 if any(s in full_url.lower() for s in shorteners) else 1
        elif col == "having_At_Symbol":
            features[col] = -1 if "@" in full_url else 1
        elif col == "double_slash_redirecting":
            features[col] = -1 if full_url.rfind("//") > 7 else 1
        elif col == "Prefix_Suffix":
            features[col] = -1 if "-" in hostname else 1
        elif col == "having_Sub_Domain":
            dot_count = hostname.count(".")
            if dot_count <= 1:
                features[col] = 1
            elif dot_count == 2:
                features[col] = 0
            else:
                features[col] = -1
        elif col == "SSLfinal_State":
            features[col] = 1 if scheme == "https" else -1
        elif col == "Domain_registeration_length":
            features[col] = -1
        elif col == "Favicon":
            features[col] = 1
        elif col == "port":
            standard_ports = [80, 443, None]
            features[col] = 1 if parsed and parsed.port in standard_ports else -1
        elif col == "HTTPS_token":
            features[col] = -1 if "https" in hostname.lower() else 1
        elif col == "Request_URL":
            features[col] = 1
        elif col == "URL_of_Anchor":
            features[col] = 1
        elif col == "Links_in_tags":
            features[col] = 1
        elif col == "SFH":
            features[col] = 1
        elif col == "Submitting_to_email":
            features[col] = -1 if "mailto:" in full_url.lower() else 1
        elif col == "Abnormal_URL":
            features[col] = 1 if hostname and hostname in full_url else -1
        elif col == "Redirect":
            features[col] = 0
        elif col == "on_mouseover":
            features[col] = 1
        elif col == "RightClick":
            features[col] = 1
        elif col == "popUpWidnow":
            features[col] = 1
        elif col == "Iframe":
            features[col] = 1
        elif col == "age_of_domain":
            features[col] = -1
        elif col == "DNSRecord":
            features[col] = -1
        elif col == "web_traffic":
            features[col] = -1
        elif col == "Page_Rank":
            features[col] = -1
        elif col == "Google_Index":
            features[col] = 1
        elif col == "Links_pointing_to_page":
            features[col] = 0
        elif col == "Statistical_report":
            features[col] = 1
        else:
            features[col] = 0

    return features


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/detect")

@app.get("/detect")
async def detect_page(request: Request):
    return templates.TemplateResponse("table.html", {"request": request, "table": ""})

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e,sys)

@app.post("/predict")
async def predict_route(request: Request,file: UploadFile = File(...)):
    try:
        df=pd.read_csv(file.file)
        preprocesor=load_object("final_model/preprocessor.pkl")
        final_model=load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocesor,model=final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        df.to_csv('prediction_output/output.csv')
        table_html = df.to_html(classes='table table-striped')
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})

    except Exception as e:
            raise NetworkSecurityException(e,sys)


@app.post("/predict-url")
async def predict_url(request: URLRequest):
    try:
        if not os.path.exists("final_model/model.pkl") or not os.path.exists("final_model/preprocessor.pkl"):
            return JSONResponse(
                status_code=400,
                content={"error": "Model not trained yet. Please run training first."}
            )

        csv_path = "Network_Data/phisingData.csv"
        df_schema = pd.read_csv(csv_path, nrows=0)
        feature_columns = [c for c in df_schema.columns.tolist() if c != "Result"]

        features = extract_features_from_url(request.url, feature_columns)
        input_df = pd.DataFrame([features])

        preprocessor = load_object("final_model/preprocessor.pkl")
        model = load_object("final_model/model.pkl")

        input_transformed = preprocessor.transform(input_df)
        prediction = model.predict(input_transformed)

        confidence = 0.50
        try:
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(input_transformed)
                confidence = float(np.max(proba))
            elif hasattr(model, "decision_function"):
                decision = model.decision_function(input_transformed)
                confidence = float(1 / (1 + np.exp(-abs(decision[0]))))
        except Exception:
            confidence = 0.50

        pred_value = int(prediction[0])
        label = "Phishing" if pred_value == 0 else "Legitimate"

        return JSONResponse(content={
            "url": request.url,
            "prediction": label,
            "confidence": round(confidence, 4)
        })

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Prediction failed: {str(e)}"}
        )


class FeaturesRequest(BaseModel):
    features: dict


@app.get("/model-info")
async def model_info():
    try:
        if not os.path.exists("final_model/model.pkl"):
            return JSONResponse(status_code=400, content={"error": "Model not trained yet."})

        model = load_object("final_model/model.pkl")
        csv_path = "Network_Data/phisingData.csv"
        df_schema = pd.read_csv(csv_path, nrows=0)
        feature_columns = [c for c in df_schema.columns.tolist() if c != "Result"]

        importances = []
        if hasattr(model, "feature_importances_"):
            raw = model.feature_importances_.tolist()
            paired = list(zip(feature_columns, raw))
            paired.sort(key=lambda x: x[1], reverse=True)
            importances = [{"feature": f, "importance": round(v, 5)} for f, v in paired]

        df_full = pd.read_csv(csv_path)
        total = len(df_full)
        phishing_count = int((df_full["Result"] == -1).sum())
        legit_count = int((df_full["Result"] == 1).sum())

        return JSONResponse(content={
            "features": feature_columns,
            "importances": importances,
            "dataset": {
                "total": total,
                "phishing": phishing_count,
                "legitimate": legit_count
            }
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/predict-features")
async def predict_features(request: FeaturesRequest):
    try:
        if not os.path.exists("final_model/model.pkl"):
            return JSONResponse(status_code=400, content={"error": "Model not trained yet."})

        preprocessor = load_object("final_model/preprocessor.pkl")
        model = load_object("final_model/model.pkl")

        input_df = pd.DataFrame([request.features])
        input_transformed = preprocessor.transform(input_df)
        prediction = model.predict(input_transformed)

        confidence = 0.50
        try:
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(input_transformed)
                confidence = float(np.max(proba))
        except Exception:
            confidence = 0.50

        pred_value = int(prediction[0])
        label = "Phishing" if pred_value == 0 else "Legitimate"

        return JSONResponse(content={
            "prediction": label,
            "confidence": round(confidence, 4)
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)
