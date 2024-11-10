import pandas as pd
import boto3
import os
from src.utils import load_config
import os
import logging
import sys
import argparse


logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("extraction")

session = boto3.Session(profile_name='personal')

s3 = session.client('s3')

def download_files_from_s3(config):
    bucket_name = config['extraction']['bucket_name']
    download_directory = config['extraction']['download_directory']
    paginator = s3.get_paginator('list_objects_v2')
    operation_parameters = {'Bucket': bucket_name,
                        'Prefix': 'carros/'}
    for page in paginator.paginate(**operation_parameters):
        for obj in page.get('Contents', []):
            local_file_path = os.path.join(download_directory, obj['Key'])
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            try:
                s3.download_file(bucket_name, obj['Key'], local_file_path)
                print(f"Descargado: {local_file_path}")
            except: 
                print('Archivo no descargable')


def main(config_path):
    config = load_config(config_path)
    download_files_from_s3(config)


# Llama a la función para descargar los archivos
if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--config", dest="config", required=True)
    args = args_parser.parse_args()
    main(args.config)