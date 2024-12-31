from src.constants import *
from src.config.configuration import *
import os, sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
from src.components.data_transformation import DataTransformation, DataTransformationConfig
from src.components.model_trainer import ModelTrainer

@dataclass
class DataIngestionConfig:
    train_data_path: str = TRAIN_FILE_PATH
    test_data_path: str = TEST_FILE_PATH
    raw_data_path: str = RAW_FILE_PATH

class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        try:
            logging.info("Reading the dataset from path...")
            df = pd.read_csv(DATASET_PATH)

            logging.info("Saving the raw dataset to file...")
            os.makedirs(os.path.dirname(self.data_ingestion_config.raw_data_path), exist_ok=True)
            df.to_csv(self.data_ingestion_config.raw_data_path, index=False)

            logging.info("Splitting dataset into train and test sets...")
            train_set, test_set = train_test_split(df, test_size=0.20, random_state=42)

            logging.info("Saving the train and test datasets to file...")
            os.makedirs(os.path.dirname(self.data_ingestion_config.train_data_path), exist_ok=True)
            train_set.to_csv(self.data_ingestion_config.train_data_path, index=False)

            os.makedirs(os.path.dirname(self.data_ingestion_config.test_data_path), exist_ok=True)
            test_set.to_csv(self.data_ingestion_config.test_data_path, index=False)

            logging.info("Data ingestion completed successfully.")
            return (
                self.data_ingestion_config.train_data_path,
                self.data_ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)

# Main Execution
if __name__ == "__main__":
    try:
        logging.info("Starting data ingestion process...")
        obj = DataIngestion()
        train_data_path, test_data_path = obj.initiate_data_ingestion()

        logging.info("Starting data transformation process...")
        data_transformation = DataTransformation()
        train_arr, test_arr, _ = data_transformation.inititate_data_transformation(
            train_data_path, test_data_path
        )

        logging.info("Starting model training process...")
        model_trainer = ModelTrainer()
        print(model_trainer.inititate_model_traing(train_arr, test_arr))

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
