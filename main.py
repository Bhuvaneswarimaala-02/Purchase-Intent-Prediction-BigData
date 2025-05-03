# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import Literal
# from pyspark.sql import SparkSession
# from pyspark.ml.pipeline import PipelineModel

# # Initialize FastAPI
# app = FastAPI()

# # Start Spark Session
# spark = SparkSession.builder \
#     .appName("FastAPIModel") \
#     .config("spark.driver.memory", "2g") \
#     .getOrCreate()

# # Load trained model
# model = PipelineModel.load("model_rf")

# # Input schema
# class InputData(BaseModel):
#     Administrative: int
#     Administrative_Duration: float
#     Informational: int
#     Informational_Duration: float
#     ProductRelated: int
#     ProductRelated_Duration: float
#     BounceRates: float
#     ExitRates: float
#     PageValues: float
#     SpecialDay: float
#     Month: str
#     VisitorType: str
#     Weekend: Literal["True", "False"]


# @app.post("/predict")
# def predict(data: InputData):
#     # Convert input to DataFrame
#     input_dict = data.dict()
#     input_df = spark.createDataFrame([input_dict])

#     # Predict
#     prediction = model.transform(input_df)
#     result = prediction.select("prediction").collect()[0][0]

#     # Return result
#     return {"prediction": int(result)}



import os
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
from pyspark.sql import SparkSession
from pyspark.ml.pipeline import PipelineModel
import uvicorn

# Initialize FastAPI
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}

# Configure logging
logging.basicConfig(level=logging.INFO)

# Start Spark Session
spark = SparkSession.builder \
    .appName("FastAPIModel") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()

# Load trained model
try:
    model = PipelineModel.load("model_rf")
    logging.info("Model loaded successfully")
except Exception as e:
    logging.error(f"Error loading model: {e}")
    model = None

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
    if model is None:
        return {"error": "Model not loaded correctly, please check the deployment logs."}
    
    try:
        # Convert input to DataFrame
        input_dict = data.dict()
        input_df = spark.createDataFrame([input_dict])

        # Predict
        prediction = model.transform(input_df)
        result = prediction.select("prediction").collect()[0][0]

        # Return result
        return {"prediction": int(result)}

    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Use the port provided by Render, default to 10000
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
