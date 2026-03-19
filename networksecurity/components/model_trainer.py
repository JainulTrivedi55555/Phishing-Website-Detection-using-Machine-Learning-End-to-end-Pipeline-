# import os
# import sys
# from urllib.parse import urlparse

# import mlflow

# from networksecurity.exception.exception import NetworkSecurityException 
# from networksecurity.logging.logger import logging

# from networksecurity.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
# from networksecurity.entity.config_entity import ModelTrainerConfig



# from networksecurity.utils.ml_utils.model.estimator import NetworkModel
# from networksecurity.utils.main_utils.utils import save_object,load_object
# from networksecurity.utils.main_utils.utils import load_numpy_array_data,evaluate_models
# from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

# from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import r2_score
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import (
#     AdaBoostClassifier,
#     GradientBoostingClassifier,
#     RandomForestClassifier,
# )

# import dagshub
# dagshub.init(repo_owner='JainulTrivedi55555', repo_name='Networksecurity', mlflow=True)

# # os.environ["MLFLOW_TRACKING_URI"]="https://dagshub.com/krishnaik06/networksecurity.mlflow"
# # os.environ["MLFLOW_TRACKING_USERNAME"]="krishnaik06"
# # os.environ["MLFLOW_TRACKING_PASSWORD"]="7104284f1bb44ece21e0e2adb4e36a250ae3251f"





# class ModelTrainer:
#     def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
#         try:
#             self.model_trainer_config=model_trainer_config
#             self.data_transformation_artifact=data_transformation_artifact
#         except Exception as e:
#             raise NetworkSecurityException(e,sys)
        
#     def track_mlflow(self,best_model,classificationmetric):
#         mlflow.set_registry_uri("https://dagshub.com/krishnaik06/networksecurity.mlflow")
#         tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
#         with mlflow.start_run():
#             f1_score=classificationmetric.f1_score
#             precision_score=classificationmetric.precision_score
#             recall_score=classificationmetric.recall_score

            

#             mlflow.log_metric("f1_score",f1_score)
#             mlflow.log_metric("precision",precision_score)
#             mlflow.log_metric("recall_score",recall_score)
#             mlflow.sklearn.log_model(best_model,"model")
#             # Model registry does not work with file store
#             if tracking_url_type_store != "file":

#                 # Register the model
#                 # There are other ways to use the Model Registry, which depends on the use case,
#                 # please refer to the doc for more information:
#                 # https://mlflow.org/docs/latest/model-registry.html#api-workflow
#                 mlflow.sklearn.log_model(best_model, "model", registered_model_name=best_model)
#             else:
#                 mlflow.sklearn.log_model(best_model, "model")


        
#     def train_model(self,X_train,y_train,x_test,y_test):
#         models = {
#                 "Random Forest": RandomForestClassifier(verbose=1),
#                 "Decision Tree": DecisionTreeClassifier(),
#                 "Gradient Boosting": GradientBoostingClassifier(verbose=1),
#                 "Logistic Regression": LogisticRegression(verbose=1),
#                 "AdaBoost": AdaBoostClassifier(),
#             }
#         params={
#             "Decision Tree": {
#                 'criterion':['gini', 'entropy', 'log_loss'],
#                 # 'splitter':['best','random'],
#                 # 'max_features':['sqrt','log2'],
#             },
#             "Random Forest":{
#                 # 'criterion':['gini', 'entropy', 'log_loss'],
                
#                 # 'max_features':['sqrt','log2',None],
#                 'n_estimators': [8,16,32,128,256]
#             },
#             "Gradient Boosting":{
#                 # 'loss':['log_loss', 'exponential'],
#                 'learning_rate':[.1,.01,.05,.001],
#                 'subsample':[0.6,0.7,0.75,0.85,0.9],
#                 # 'criterion':['squared_error', 'friedman_mse'],
#                 # 'max_features':['auto','sqrt','log2'],
#                 'n_estimators': [8,16,32,64,128,256]
#             },
#             "Logistic Regression":{},
#             "AdaBoost":{
#                 'learning_rate':[.1,.01,.001],
#                 'n_estimators': [8,16,32,64,128,256]
#             }
            
#         }
#         model_report:dict=evaluate_models(X_train=X_train,y_train=y_train,X_test=x_test,y_test=y_test,
#                                           models=models,param=params)
        
#         ## To get best model score from dict
#         best_model_score = max(sorted(model_report.values()))

#         ## To get best model name from dict

#         best_model_name = list(model_report.keys())[
#             list(model_report.values()).index(best_model_score)
#         ]
#         best_model = models[best_model_name]
#         y_train_pred=best_model.predict(X_train)

#         classification_train_metric=get_classification_score(y_true=y_train,y_pred=y_train_pred)

        
#         ## Track the experiements with mlflow
#         self.track_mlflow(best_model,classification_train_metric)


#         y_test_pred=best_model.predict(x_test)
#         classification_test_metric=get_classification_score(y_true=y_test,y_pred=y_test_pred)

#         self.track_mlflow(best_model,classification_test_metric)

#         preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            
#         model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
#         os.makedirs(model_dir_path,exist_ok=True)

#         Network_Model=NetworkModel(preprocessor=preprocessor,model=best_model)
#         save_object(self.model_trainer_config.trained_model_file_path,obj=NetworkModel)
#         #model pusher
#         save_object("final_model/model.pkl",best_model)
        

#         ## Model Trainer Artifact
#         model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
#                              train_metric_artifact=classification_train_metric,
#                              test_metric_artifact=classification_test_metric
#                              )
#         logging.info(f"Model trainer artifact: {model_trainer_artifact}")
#         return model_trainer_artifact


        


       
    
    
        
#     def initiate_model_trainer(self)->ModelTrainerArtifact:
#         try:
#             train_file_path = self.data_transformation_artifact.transformed_train_file_path
#             test_file_path = self.data_transformation_artifact.transformed_test_file_path

#             #loading training array and testing array
#             train_arr = load_numpy_array_data(train_file_path)
#             test_arr = load_numpy_array_data(test_file_path)

#             x_train, y_train, x_test, y_test = (
#                 train_arr[:, :-1],
#                 train_arr[:, -1],
#                 test_arr[:, :-1],
#                 test_arr[:, -1],
#             )

#             model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)
#             return model_trainer_artifact

            
#         except Exception as e:
#             raise NetworkSecurityException(e,sys)




import os
import sys
import pickle # Added this import
from urllib.parse import urlparse

import dagshub
import mlflow

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_object, load_object
from networksecurity.utils.main_utils.utils import load_numpy_array_data, evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from dotenv import load_dotenv
load_dotenv()

# Using environment variables is the recommended way to configure MLflow tracking.
# Ensure these are set in your environment or a config file, not hardcoded here.
# os.environ["MLFLOW_TRACKING_URI"]="https://dagshub.com/krishnaik06/networksecurity.mlflow"
# os.environ["MLFLOW_TRACKING_USERNAME"]="krishnaik06"
# os.environ["MLFLOW_TRACKING_PASSWORD"]="7104284f1bb44ece21e0e2adb4e36a250ae3251f"

# The dagshub.init call can be problematic with some MLflow tracking servers.
# It's better to rely on the environment variables above.
# os.environ["MLFLOW_TRACKING_URI"] = "https://dagshub.com/JainulTrivedi55555/Networksecurity.mlflow"
# os.environ["MLFLOW_TRACKING_USERNAME"] = "JainulTrivedi55555"
# os.environ["MLFLOW_TRACKING_PASSWORD"] = "31029266a567cd1f528d87598713d18424134976"

# dagshub.init(repo_owner='JainulTrivedi55555', repo_name='Networksecurity', mlflow=True)

class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def track_mlflow(self, best_model, classification_train_metric, classification_test_metric):
        logging.info("Starting MLflow tracking run...")
        # Note: mlflow.set_registry_uri is often redundant if environment variables are set correctly
        # mlflow.set_registry_uri("https://dagshub.com/krishnaik06/networksecurity.mlflow")

        with mlflow.start_run():
            # Log train metrics
            mlflow.log_metric("train_f1_score", classification_train_metric.f1_score)
            mlflow.log_metric("train_precision", classification_train_metric.precision_score)
            mlflow.log_metric("train_recall_score", classification_train_metric.recall_score)
            
            # Log test metrics
            mlflow.log_metric("test_f1_score", classification_test_metric.f1_score)
            mlflow.log_metric("test_precision", classification_test_metric.precision_score)
            mlflow.log_metric("test_recall_score", classification_test_metric.recall_score)

            # --- START OF FIX ---
            # The original code `mlflow.sklearn.log_model` was causing the error.
            # We will now save the model as a pickle file and log the file as an artifact.
            logging.info("Attempting to log model as a file artifact to handle DagsHub API incompatibility.")
            model_path = "best_model.pkl"
            
            # Save the model locally using pickle
            with open(model_path, "wb") as f:
                pickle.dump(best_model, f)
            
            # Log the locally saved model as an artifact to MLflow
            mlflow.log_artifact(model_path)
            
            # Clean up the temporary local file
            os.remove(model_path)
            logging.info("Successfully logged the model as a file artifact.")
            # --- END OF FIX ---
        
        logging.info("MLflow tracking run completed.")

    def train_model(self, X_train, y_train, x_test, y_test):
        models = {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "AdaBoost": AdaBoostClassifier(),
        }
        params = {
            "Decision Tree": {
                'criterion': ['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest": {
                # 'criterion':['gini', 'entropy', 'log_loss'],
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8, 16, 32, 128, 256]
            },
            "Gradient Boosting": {
                # 'loss':['log_loss', 'exponential'],
                'learning_rate': [.1, .01, .05, .001],
                'subsample': [0.6, 0.7, 0.75, 0.85, 0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8, 16, 32, 64, 128, 256]
            },
            "Logistic Regression": {},
            "AdaBoost": {
                'learning_rate': [.1, .01, .001],
                'n_estimators': [8, 16, 32, 64, 128, 256]
            }
        }
        model_report: dict = evaluate_models(X_train=X_train, y_train=y_train, X_test=x_test, y_test=y_test,
                                             models=models, param=params)

        ## To get best model score from dict
        best_model_score = max(sorted(model_report.values()))

        ## To get best model name from dict
        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]
        best_model = models[best_model_name]
        
        y_train_pred = best_model.predict(X_train)
        classification_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)

        y_test_pred = best_model.predict(x_test)
        classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)

        # We now pass both train and test metrics to the track_mlflow function.
        self.track_mlflow(best_model, classification_train_metric, classification_test_metric)

        preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path, exist_ok=True)

        Network_Model = NetworkModel(preprocessor=preprocessor, model=best_model)
        # Saving the final model object (which includes the preprocessor) to the correct path
        save_object(self.model_trainer_config.trained_model_file_path, obj=Network_Model)
        logging.info(f"Trained model saved to: {self.model_trainer_config.trained_model_file_path}")

        # NOTE: The hardcoded path below has been removed to avoid a file path mismatch.
        # save_object("final_model/model.pkl", best_model)

        ## Model Trainer Artifact
        model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                                      train_metric_artifact=classification_train_metric,
                                                      test_metric_artifact=classification_test_metric)
        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        return model_trainer_artifact

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            #loading training array and testing array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model_trainer_artifact = self.train_model(x_train, y_train, x_test, y_test)
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
