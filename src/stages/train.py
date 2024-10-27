import joblib
import argparse
from pycaret.regression import *
from xgboost import XGBRegressor
from typing import Text
from src.utils import load_config, load_train_datasets
import logging
import sys

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(name)s: %(message)s',
    level=logging.INFO,
    datefmt='%H:%M:%S',
    stream=sys.stderr
)
logger = logging.getLogger('Train')

def run_model_training(config_path: Text):
    config = load_config(config_path)
    logger.info('Init Feature Selection!')
    logger.info('Init Model Training!')
    X_train_transformed, X_test_transformed = load_train_datasets(config)
    logger.info('Loading Feature Engineering pipeline')
    preprocess_pipeline = joblib.load(config['feature_engineering']['pipeline'])
    setup_model = setup(data= X_train_transformed,
                        target = config['featurize']['target_column'],
                        session_id = 0,
                        preprocess = False,
                        test_data = X_test_transformed,
                        verbose=False,
                        index=True
                    )
    logger.info('Comparing All Classification Models')
    best = compare_models(sort = 'r2')
    logger.info('Saving All Models Experiment')
    best_tuned_model = tune_model(best, fold=5, n_iter=5)
    preprocess_pipeline.steps.append(('best_model',best_tuned_model))
    predictions = predict_model(best_tuned_model, X_test_transformed)
    #experiments = pull()
    #experiments.iloc[0,:].to_json(config['evaluate']['metrics'])
    logger.info('Saving Complete Pipeline!')
    joblib.dump(preprocess_pipeline, config['train']['final_model'])
    logger.info('Finalized Model Training!')


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config', dest='config', required=True)
    args = args_parser.parse_args()
    run_model_training(args.config)