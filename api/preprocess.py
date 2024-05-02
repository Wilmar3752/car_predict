from datetime import datetime
import pandas as pd

now = datetime.now().year

def get_antique(vehicle_model):
    antique = now - vehicle_model
    return antique

def prepare_model_input(raw_model_input):
    df = pd.json_normalize(raw_model_input)
    df['antique'] = get_antique(df['vehicle_model'])
    df = df.drop(columns='vehicle_model')
    return df