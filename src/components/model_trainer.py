from src.constants import *
from src.logger import logging
from src.exception import CustomException
import os, sys
from src.config.configuration import *
from dataclasses import dataclass
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd

# Import libraries for regression models
from xgboost import XGBRegressor  # XGBoost Regressor
from sklearn.tree import DecisionTreeRegressor  # Decision Tree Regressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor  # Gradient Boosting & Random Forest Regressors
from sklearn.svm import SVR  # Support Vector Regressor (SVR)

from src.utils import evaluate_model, save_obj

# Additional libraries for dataset loading, model training, and evaluation
from sklearn.model_selection import train_test_split  # For splitting the dataset
from sklearn.metrics import mean_squared_error  # For calculating Mean Squared Error (MSE)

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = MODEL_FILE_PATH

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig

    def inititate_model_traing(self, train_array, test_array):
        try:
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1], train_array[:, -1],
                test_array[:, :-1], test_array[:, -1]
            )

            models = {
                "XGBRegressor": XGBRegressor(),
                "DecisionTreeRegressor": DecisionTreeRegressor(),
                "GradientBoostingRegressor": GradientBoostingRegressor(),
                "RandomForestRegressor": RandomForestRegressor(),
                "SVR": SVR()
            }

            # Evaluate models and get scores
            model_report: dict = evaluate_model(X_train, y_train, X_test, y_test, models)
            print(model_report)

            # Find the best model
            best_model_name = max(model_report, key=model_report.get)  # Get the key with the highest value
            best_model_score = model_report[best_model_name]           # Get the corresponding score

            best_model = models[best_model_name]

            print(f"Best Model Found, Model Name: {best_model_name}, R2_Score: {best_model_score}")
            logging.info(f"Best Model Found, Model Name: {best_model_name}, R2_Score: {best_model_score}")

            # Save the best model
            save_obj(file_path=self.model_trainer_config.trained_model_file_path, obj=best_model)

        except Exception as e:
            raise CustomException(e, sys)
