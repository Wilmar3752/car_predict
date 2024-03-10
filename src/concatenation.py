import pandas as pd
import glob
import os

def csv_concatenation(input_path):
    all_files = glob.glob(os.path.join(input_path, "*.csv"))

    li = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=0)
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True).drop_duplicates(subset='id', keep='last')
    return frame

def delete_unused_files(input_path):


    # Get a list of all files in the directory
    files = glob.glob(input_path + "/*")

    # Iterate over the list of files
    for file in files:
        # Check if the current file is not 'car_raw.csv'
        if os.path.basename(file) != 'car_raw.csv':
            # Delete the file
            os.remove(file)


# Llama a la función para descargar los archivos
if __name__ == "__main__":
    data_path = "data/raw"
    final_data = csv_concatenation(data_path)
    final_data.to_csv("data/raw/car_raw.csv")
    delete_unused_files(data_path)
