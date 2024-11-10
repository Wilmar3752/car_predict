import argparse
import joblib
import json
import pandas as pd
from pathlib import Path
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from typing import Text, Dict
import numpy as np
import yaml
import logging
import sys
from src.utils.utils import load_config

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(name)s: %(message)s',
    level=logging.INFO,
    datefmt='%H:%M:%S',
    stream=sys.stderr
)

logger = logging.getLogger('Evaluate')

def evaluate_model(config_path: Text) -> None:
    """Evaluate model.
    Args:
        config_path {Text}: path to config
    """

    config = load_config(config_path)

    logger.info('Load model')
    model_path = config['train']['final_model']
    model = joblib.load(model_path)

    logger.info('Load test dataset')
    test_df = pd.read_csv(config['data_split']['testset_path'], index_col=config['featurize']['index_col'])
    train_df = pd.read_csv(config['data_split']['trainset_path'], index_col=config['featurize']['index_col'])

    logger.info('Evaluate (build report)')
    target_column=config['featurize']['target_column']
    y_test = test_df.loc[:, target_column]
    X_test = test_df.drop(target_column, axis=1)

    y_train = train_df.loc[:, target_column]
    X_train = train_df.drop(target_column, axis=1)

    # Predicciones del modelo
    y_pred = model.predict(X_test)
    y_pred_train = model.predict(X_train)

    # Métricas de regresión
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    mse_train = mean_squared_error(y_train, y_pred_train)
    mae_train = mean_absolute_error(y_train, y_pred_train)
    r2_train = r2_score(y_train, y_pred_train)

    report = {
        'mse': mse,
        'mae': mae,
        'r2': r2,
        'actual': y_test.tolist(),
        'predicted': y_pred.tolist(),
        'model_name': model[-1].__class__.__name__,
        'mse_train': mse_train,
        'mae_train': mae_train,
        'r2_train': r2_train
    }

    logger.info('Save metrics')
    reports_folder = Path(config['base']['reports_dir'])
    metrics_path = reports_folder / config['evaluate']['metrics']
    json.dump(
        obj={
            'model_name': report['model_name'],
            'mse': report['mse'],
            'mae': report['mae'],
            'r2': report['r2'],
            'r2_train': report['r2_train']
        },
        fp=open(metrics_path, 'w')
    )

    logger.info(f'Metrics file saved to: {metrics_path}')

    # logger.info('Save regression results plot')
    # plt = plot_regression_results(y_test, y_pred)
    # regression_results_png_path = reports_folder / config['evaluate']['regression_results_plot']
    # plt.savefig(regression_results_png_path)
    # logger.info(f'Regression results plot saved to: {regression_results_png_path}')

if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config', dest='config', required=True)
    args = args_parser.parse_args()
    evaluate_model(args.config)