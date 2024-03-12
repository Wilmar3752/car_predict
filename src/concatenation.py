import pandas as pd
import glob
import os
from src.utils import load_config
import logging
import sys
import argparse

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("concatenation")

def csv_concatenation(config):
    logger.info('concatenando data')
    input_path = config['concatenation']['input_path']
    all_files = glob.glob(os.path.join(input_path, "*.csv"))
    li = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=0)
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True).drop_duplicates(subset='id', keep='last')
    return frame

def delete_unused_files(config):
    logger.info('borrando archivos innecesarios')
    input_path = config['concatenation']['input_path']
    # Get a list of all files in the directory
    files = glob.glob(input_path + "/*")

    # Iterate over the list of files
    for file in files:
        # Check if the current file is not 'car_raw.csv'
        if os.path.basename(file) != 'car_raw.csv':
            # Delete the file
            os.remove(file)

def main(config_path: str):
    config = load_config(config_path)
    output_path = config['concatenation']['output_path']
    output_filename = output_path + "/" + config['concatenation']['output_filename']
    final_data = csv_concatenation(config)
    final_data.to_csv(output_filename)
    delete_unused_files(config)



# Llama a la función para descargar los archivos
if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--config", dest="config", required=True)
    args = args_parser.parse_args()
    main(args.config)
