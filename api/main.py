import pandas as pd
import joblib
import json
import time
from api.business_layer import RequestBody, ResponseBody
from api.preprocess import get_antique, prepare_model_input
from fastapi import FastAPI

model = joblib.load('models/final_pipeline.joblib')

app = FastAPI()

@app.post("/predict", response_model = ResponseBody)
def predict(input: RequestBody):
        # preprocessing
    start = time.perf_counter_ns()
    df = prepare_model_input(input.model_dump(mode="json"))
    end = time.perf_counter_ns()
    prediction = model.predict(df)
    preprocessing_time_ms = (end - start) / 1_000_000
    output = {
        'expected_price': prediction,
        'request_body': input.model_dump(mode='json'),
        'prediction_time_ms': preprocessing_time_ms
    }
    return output

@app.get("/heart-beat")
async def service_health():
    return {"ok"}

