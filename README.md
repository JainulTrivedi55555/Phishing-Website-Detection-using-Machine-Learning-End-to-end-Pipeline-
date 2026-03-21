# Phishing Website Detection

A machine learning pipeline that classifies websites as phishing or legitimate based on URL and domain-level features. The raw data lives in MongoDB, gets pulled through a multi-stage training pipeline, and is served via a FastAPI app — all containerized with Docker and backed by a GitHub Actions CI workflow.

---

## How it works

**Data flow:**

1. **push_data.py** — converts the raw CSV into JSON and pushes it to a MongoDB collection
2. **Data Ingestion** — pulls data from MongoDB, saves it locally, splits into train/test
3. **Data Validation** — checks column counts and runs a KS test to detect data drift between train and test sets
4. **Data Transformation** — handles missing values using KNN imputation via an sklearn pipeline
5. **Model Training** — trains 5 classifiers with GridSearchCV, picks the best by F1 score, tracks all runs with MLflow on DagsHub
6. **Model Evaluation** — compares the newly trained model against the existing production model
7. **Model Pusher** — copies the winning model and preprocessor into `final_model/`

At inference time, the FastAPI app loads the saved model and preprocessor from `final_model/`, accepts a CSV upload, and returns predictions.

---

## Models compared

Random Forest, Decision Tree, Gradient Boosting, Logistic Regression, AdaBoost — all tuned with GridSearchCV and evaluated on F1, precision, and recall.

---

## Stack

Python · scikit-learn · FastAPI · MongoDB · pymongo · MLflow · DagsHub · Docker · GitHub Actions · dill · pandas · numpy

---

## Run it locally

**1. Clone and install**
```bash
git clone https://github.com/JainulTrivedi55555/Phishing-Website-Detection-using-Machine-Learning-End-to-end-Pipeline.git
cd Phishing-Website-Detection-using-Machine-Learning-End-to-end-Pipeline
pip install -r requirements.txt
pip install -e .
```

**2. Set up your environment variables**

Create a `.env` file at the root:
```
MONGO_DB_URL=your_mongodb_connection_string
```

**3. Push data to MongoDB**
```bash
python push_data.py
```

**4. Run the training pipeline**
```bash
python main.py
```

**5. Start the API**
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Or with Docker:
```bash
docker build -t phishing-detector .
docker run -p 8000:8000 --env-file .env phishing-detector
```

Then open `http://localhost:8000/docs` to use the interactive API.

---

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Redirects to `/docs` |
| GET | `/train` | Triggers the full training pipeline |
| POST | `/predict` | Upload a CSV, get predictions back |

---

## Project layout

```
├── app.py                         # FastAPI app
├── main.py                        # Runs the full training pipeline
├── push_data.py                   # Loads CSV into MongoDB
├── setup.py
├── requirements.txt
├── Dockerfile
│
├── networksecurity/
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   ├── model_trainer.py
│   │   ├── model_evaluation.py
│   │   └── model_pusher.py
│   ├── pipeline/
│   │   ├── training_pipeline.py
│   │   └── batch_prediction.py
│   ├── entity/
│   │   ├── config_entity.py
│   │   └── artifact_entity.py
│   ├── constant/
│   │   ├── application_constant.py
│   │   └── training_pipeline/
│   ├── utils/
│   │   ├── main_utils/
│   │   │   └── utils.py
│   │   └── ml_utils/
│   │       ├── metric/
│   │       │   └── classification_metric.py
│   │       └── model/
│   │           └── estimator.py
│   ├── cloud/
│   │   └── s3_sync.py
│   ├── exception/
│   │   └── exception.py
│   └── logging/
│       └── logger.py
│
├── Network_Data/
│   └── phisingData.csv
│
├── data_schema/
│   └── schema.yaml
│
├── final_model/
│   ├── model.pkl
│   └── preprocessor.pkl
│
├── valid_data/
│   └── test.csv
│
├── templates/
│   └── table.html
│
└── .github/
    └── workflows/
        └── main.yml
```
