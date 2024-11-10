from pydantic import BaseModel, Field

class RequestBody(BaseModel):
    # required for all AI models
    vehicle_model: int = 2014
    # Model specific
    vehicle_make: str = "Kia"
    vehicle_line: str = "Cerato"
    version: str = "Pro 1.6 Sx"
    kilometraje: int =  50000
    #location_city: str = "Suba"
    #location_state: str = "Bogotá D.C."


class ResponseBody(BaseModel):
    expected_price: float
    request_body: dict
    prediction_time_ms: float
