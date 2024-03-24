import os
import yaml
import logging
import sys
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import pandas as pd


logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)


def load_config(config_name):
    logger.info("Loading Config File")
    with open(os.path.join(config_name)) as file:
        config = yaml.safe_load(file)
    return config

def save_datasets(X_train, y_train, X_test, y_test, pipeline, config):
    X_train_transformed = pipeline.transform(X_train)
    X_test_transformed = pipeline.transform(X_test)

    X_train[config['featurize']['target_column']] = y_train
    X_test[config['featurize']['target_column']] = y_test
    
    X_train_transformed[config['featurize']['target_column']] = y_train    
    X_test_transformed[config['featurize']['target_column']] = y_test

    X_train.to_csv(config['featurize']['data_transformed_path'] + 'X_train.csv', index=True)
    X_test.to_csv(config['featurize']['data_transformed_path'] + 'X_test.csv', index=True)
    X_train_transformed.to_csv(config['featurize']['data_transformed_path'] + 'X_train_transformed.csv', index=True)
    X_test_transformed.to_csv(config['featurize']['data_transformed_path'] + 'X_test_tranformed.csv', index=True)

def load_train_datasets(config):
    logger.info('Loading transformed training and test sets')
    X_train = pd.read_csv(config['featurize']['data_transformed_path'] + 'X_train_transformed.csv', index_col=config['featurize']['index_col'])
    X_test = pd.read_csv(config['featurize']['data_transformed_path'] + 'X_test_tranformed.csv', index_col=config['featurize']['index_col'])
    return X_train, X_test



class ScalerDf(BaseEstimator, TransformerMixin):

    def __init__(self, method):
        self.method = method

    def transform(self, X):
        X = pd.DataFrame(
            self.scaler.transform(X),
            columns=X.columns,
            index=X.index
        )
        return X

    def fit(self, X, y=None):
        if self.method == 'minmax':
            self.scaler = MinMaxScaler()
        elif self.method == 'standard':
            self.scaler = StandardScaler()
        elif self.method == 'none':
            return self
        else:
            raise ValueError("Invalid scaling method. Supported methods are 'minmax', 'standard', and 'none'.")

        self.scaler.fit(X)
        return self