import pandas as pd
import numpy as np
import seaborn as sns
import sys,os
from dataclasses import dataclass
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler,OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from src.exception import CustomException
from src.logger import logging
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression,Lasso,Ridge,ElasticNet
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error
from src.utils import save_object


### Data Transformation config

@dataclass
class DataTransformationconfig:
    
    preprocessor_obj_file_path = os.path.join("artifacts","preprocessor.pkl")




##Data Ingestionconfig class

class DataTransformation:
    def __init__(self):

        self.data_transformation_config = DataTransformationconfig()

    def get_data_transformation_object(self):

        try:
            logging.info("Data Transformation initiated")

            #Define which columns should be ordinal-encoded and whicxh should be scaled 
            categorical_cols = ['cut', 'color', 'clarity']
            numerical_cols = ['carat', 'depth', 'table', 'x', 'y', 'z']

            #Define the custom ranking for each ordinal variable
            cut_categories = ['Fair','Good','Very Good','Premium','Ideal']
            color_categories = ["D","E","F","G","H","I","J"]
            clarity_categories = ["I1","SI2","SI1","VS2","VS1","VVS2","VVS1","IF"]

            logging.info("Pipeline initiated")

            ##Numerical Pipeline

            num_pipeline = Pipeline(
                steps =[
                    ("imputer" ,SimpleImputer(strategy= "median")),
                    ("scaler",StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps = [
                    ("imputer",SimpleImputer(strategy = "most_frequent")),
                    ("ordinalencoder",OrdinalEncoder(categories = [cut_categories,color_categories,clarity_categories])),
                    ("scaler",StandardScaler())
                ]
            )

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_cols),
                    ("cat_pipeline",cat_pipeline,categorical_cols)
                ]
            )

            return preprocessor

            logging.info("Pipeline completed")

        except Exception as e:
            logging.info("Error in Data Transformation")
            raise CustomException(e,sys)
        

    def initiate_data_transformation(self,train_path,test_path):

        try :

            #Reading train and test data
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")
            logging.info(f"Train DataFrame Head : \n {train_df.head().to_string()}")
            logging.info(f"Test DataFrame HEad : \n {test_df.head().to_string()}")


            logging.info("Obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformation_object()

            target_columns_name = "price"
            drop_columns = [target_columns_name,"id"]

            #features into independent and dependent features

            input_feature_train_df = train_df.drop(columns= drop_columns , axis= 1)
            target_feature_train_df = train_df[target_columns_name]

            input_feature_test_df = test_df.drop(columns=drop_columns,axis = 1)
            target_feature_test_df = test_df[target_columns_name]


            # apply the transformation

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)


            logging.info("Applying preprocessing object on training and testing datasets.")


            train_arr = np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

            save_object(
                file_path= self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            logging.info("Processor pickle in created and saved")

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            logging.info("Exception occure in the initiated_datatransformation")

            raise CustomException(e,sys)




































































