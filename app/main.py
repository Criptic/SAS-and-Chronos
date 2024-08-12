import numpy as np
import pandas as pd
import torch
from chronos import ChronosPipeline
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import pandas as pd
import os
from fastapi.responses import StreamingResponse
import io
from typing import List, Dict

app = FastAPI()

class Item(BaseModel):
    prediction_length: int
    num_samples: int
    temperature: float
    top_k: int
    top_p: float
    data: List[float]

chronos_model = os.getenv('CHRONOS_MODEL')
if chronos_model is None:
    chronos_model = "amazon/chronos-t5-small"

print(f"Running using the {chronos_model} model")
pipeline = ChronosPipeline.from_pretrained(
  chronos_model,
)

# Actual prediction process
@app.post("/predict/")
async def predict(item: Item):
    try:
        prediction_length = item.prediction_length
        num_samples = item.num_samples
        temperature = item.temperature
        top_k = item.top_k
        top_p = item.top_p
        context = torch.tensor(item.data)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing input data: {e}")

    try:
        forecast = pipeline.predict(
            context,
            prediction_length,
            num_samples=num_samples,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            )
        low, median, high = np.quantile(forecast[0].numpy(), [0.1, 0.5, 0.9], axis=0)
        dfOut = pd.DataFrame(data={"low": low, "median": median, "high": high})
        stream = io.StringIO()
        dfOut.to_csv(stream, index = False)
        response = StreamingResponse(iter([stream.getvalue()]),
                                    media_type="text/csv"
                                    )
        response.headers["Content-Disposition"] = "attachment; filename=predictions.csv"
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {e}")

# Test the API endpoint
@app.get("/testPrediction/")
async def predict():
    df = pd.read_csv("https://raw.githubusercontent.com/AileenNielsen/TimeSeriesAnalysisWithPython/master/data/AirPassengers.csv")
    prediction_length = 12
    context = torch.tensor(df["#Passengers"])
    forecast = pipeline.predict(
        context,
        prediction_length,
        num_samples=20,
        temperature=1.0,
        top_k=50,
        top_p=1.0,
        )
    low, median, high = np.quantile(forecast[0].numpy(), [0.1, 0.5, 0.9], axis=0)
    dfOut = pd.DataFrame(data={"low": low, "median": median, "high": high})

    stream = io.StringIO()
    dfOut.to_csv(stream, index = False)
    response = StreamingResponse(iter([stream.getvalue()]),
                                 media_type="text/csv"
                                )
    
    response.headers["Content-Disposition"] = "attachment; filename=predictions.csv"
    return response