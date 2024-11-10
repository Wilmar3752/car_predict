import pandas as pd
from typing import Text
from src.utils.utils import load_config, save_datasets
import joblib
import argparse
import logging
import sys
from feature_engine.encoding import RareLabelEncoder, OrdinalEncoder
from src.utils import ScalerDf
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(name)s: %(message)s',
    level=logging.INFO,
    datefmt='%H:%M:%S',
    stream=sys.stderr
)
logger = logging.getLogger('Feature Engineering')


def run_feature_engineering(config_path: Text):
    # Read the selected features from the csv file
    config = load_config(config_path)
    logger.info('Init Feature Selection!')
    
    # Load the dataset using the selected features
    input_path = config['concatenation']['output_path']
    input_filename = input_path + "/" + config['concatenation']['output_filename']
    df = _read_train_dataset(input_filename)
    X_train, X_test, y_train, y_test = _train_test_split(df, config)

    pipeline = make_pipeline(X_train, config)
    # Create pipeline for feature engineering
    
    logger.info('Training Feature Engineering')
    
    # Fit the pipeline to the training data
    pipeline.fit(X_train, y_train)
    
    logger.info('Saving Feature Engineering Pipeline')
    
    # Save the pipeline to a file
    joblib.dump(pipeline, config['feature_engineering']['pipeline'])
    
    # Save the datasets
    save_datasets(X_train, y_train, X_test, y_test, pipeline, config)
    
    logger.info('Finalized Feature Engineering')

def make_pipeline(df, config):

    cat_vars = cat_vars = [var for var in df.columns if df[var].dtypes == 'O']
    # Initialize the FeatureEngineering object
    pipeline_steps = [

        ('rare_label_encoder', RareLabelEncoder(variables=cat_vars, tol=config['feature_engineering']['rarelabel_tol'], n_categories=1)),
        ('ordinal_encoder', OrdinalEncoder(variables=cat_vars)),
        ('scaler', ScalerDf(method=config['feature_engineering']['scaler_method']))
    
    ]
    pipeline = Pipeline(pipeline_steps)
    return pipeline

def _train_test_split(df, config):
    X_train, X_test, y_train, y_test = train_test_split(
    df.drop(['price'], axis=1), # predictive variables
    df['price'], # target
    test_size=config['feature_engineering']['test_size'], # portion of dataset to allocate to test set
    random_state=0, # we are setting the seed here
    )
    return X_train, X_test, y_train, y_test

def _read_train_dataset(input_filename):
    final_vars = ['price', 'antique', 'vehicle_make', 'vehicle_line','version' ,'kilometraje']
    df = pd.read_csv(input_filename,index_col=0)
    df['year_created' ] = df['_created'].apply(lambda x: x[:4]).astype(int)
    df['antique'] = df['year_created'] - df['years']
    df = df[final_vars]
    return df
# Function to run feature engineering

    
# Main entry point
if __name__ == '__main__':
    
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config', dest='config', required=True)
    args = args_parser.parse_args()

    # Call the feature engineering function
    run_feature_engineering(args.config)