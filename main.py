from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
from pyspark.sql import SparkSession
from pyspark.ml.pipeline import PipelineModel

# Initialize FastAPI
app = FastAPI()

# Start Spark Session
spark = SparkSession.builder \
    .appName("FastAPIModel") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()

# Load trained model
model = PipelineModel.load("model_rf")

# Input schema
class InputData(BaseModel):
    Administrative: int
    Administrative_Duration: float
    Informational: int
    Informational_Duration: float
    ProductRelated: int
    ProductRelated_Duration: float
    BounceRates: float
    ExitRates: float
    PageValues: float
    SpecialDay: float
    Month: str
    VisitorType: str
    Weekend: Literal["True", "False"]


@app.post("/predict")
def predict(data: InputData):
    # Convert input to DataFrame
    input_dict = data.dict()
    input_df = spark.createDataFrame([input_dict])

    # Predict
    prediction = model.transform(input_df)
    result = prediction.select("prediction").collect()[0][0]

    # Return result
    return {"prediction": int(result)}
