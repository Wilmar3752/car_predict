import pandas as pd
import boto3
import os


session = boto3.Session(profile_name='personal')

# Crear un recurso de S3 usando la sesión
s3 = session.client('s3')
def download_files_from_s3(bucket_name, download_directory):
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket_name):
        for obj in page.get('Contents', []):
            local_file_path = os.path.join(download_directory, obj['Key'])
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            s3.download_file(bucket_name, obj['Key'], local_file_path)
            print(f"Descargado: {local_file_path}")

# Llama a la función para descargar los archivos
if __name__ == "__main__":
    download_files_from_s3('scraper-meli', 'data/raw')

