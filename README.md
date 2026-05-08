# PhishGuard ML - Phishing Website Detection

A complete end-to-end machine learning system that detects phishing websites with **~96% accuracy**, built with a production-grade MLOps pipeline.

## Architecture

```
MongoDB → Schema Validation → KNN Imputer → Random Forest → MLflow → FastAPI
```

### Pipeline Stages
1. **Data Ingestion** — MongoDB Atlas, feature store, 80/20 train-test split
2. **Validation** — Schema checks, KS drift detection, YAML report
3. **Transformation** — KNN Imputer, NumPy arrays, preprocessor serialization
4. **Model Training** — GridSearchCV across 5 classifiers, MLflow experiment tracking
5. **Evaluation** — F1, Precision, Recall metrics
6. **Deployment** — FastAPI REST API with real-time predictions

### Model Comparison (GridSearchCV)

| Model | Accuracy | F1 Score | Precision | Recall |
|---|---|---|---|---|
| **Random Forest** (Selected) | ~96% | 97.1% | 96.8% | 97.4% |
| Gradient Boosting | ~95% | ~95% | ~94% | ~95% |
| AdaBoost | ~94% | ~94% | ~93% | ~94% |
| Decision Tree | ~93% | ~93% | ~92% | ~93% |
| Logistic Regression | ~91% | ~91% | ~90% | ~91% |

## Tech Stack

Python · scikit-learn · FastAPI · MongoDB · MLflow · KNN Imputer · GridSearchCV · Pandas · NumPy

## Features

- **30 URL features** analyzed per prediction
- **Live URL Analyzer** — enter any URL for instant phishing detection
- **Interactive Feature Explorer** — toggle 30 features and see real-time predictions
- **Model Dashboard** — feature importance chart, dataset distribution, analysis history
- **REST API** — JSON endpoints for programmatic access

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Push dataset to MongoDB
python push_data.py

# Train the model
python -c "from networksecurity.pipeline.training_pipeline import TrainingPipeline; TrainingPipeline().run_pipeline()"

# Start the server
python app.py
```

Open **http://localhost:8000/detect** for the full interactive UI.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/detect` | Interactive phishing detection UI |
| POST | `/predict-url` | Analyze a URL (JSON: `{"url": "..."}`) |
| POST | `/predict` | Bulk CSV prediction |
| GET | `/train` | Trigger model training |
| GET | `/model-info` | Feature importances & dataset stats |
| POST | `/predict-features` | Predict from manual feature values |

## Dataset

- **11,055 websites** with 30 URL & behavioral features
- Labels: Phishing (-1) / Legitimate (1)
- Source: UCI Phishing Websites Dataset

## Author

**Jainul Trivedi**
