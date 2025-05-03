
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler, MinMaxScaler
from pyspark.ml.classification import RandomForestClassifier

# 1. Start Spark session with memory configuration
spark = SparkSession.builder \
    .appName("OnlineShoppersIntention") \
    .config("spark.driver.memory", "4g") \
    .config("spark.executor.memory", "4g") \
    .getOrCreate()

# 2. Load CSV
df = spark.read.csv("online_shoppers_intention.csv", header=True, inferSchema=True)

# 3. Drop irrelevant columns
columns_to_drop = ["OperatingSystems", "Browser", "Region", "TrafficType"]
df = df.drop(*columns_to_drop)

# 4. Fix data types
df = df.withColumn("Weekend", col("Weekend").cast("string"))
df = df.withColumn("Revenue", col("Revenue").cast("string"))

# 5. Index categorical columns
indexers = [
    StringIndexer(inputCol="Month", outputCol="MonthIndex", handleInvalid="keep"),
    StringIndexer(inputCol="VisitorType", outputCol="VisitorTypeIndex", handleInvalid="keep"),
    StringIndexer(inputCol="Weekend", outputCol="WeekendIndex", handleInvalid="keep"),
    StringIndexer(inputCol="Revenue", outputCol="label", handleInvalid="keep")
]

# 6. One-hot encode indexed columns
encoders = [
    OneHotEncoder(inputCol="MonthIndex", outputCol="MonthVec"),
    OneHotEncoder(inputCol="VisitorTypeIndex", outputCol="VisitorTypeVec"),
    OneHotEncoder(inputCol="WeekendIndex", outputCol="WeekendVec")
]

# 7. Normalize continuous features
continuous_features = [
    "Administrative_Duration", "Informational_Duration",
    "ProductRelated_Duration", "BounceRates", "ExitRates",
    "PageValues", "SpecialDay"
]

assembler_continuous = VectorAssembler(inputCols=continuous_features, outputCol="continuous_features")
scaler = MinMaxScaler(inputCol="continuous_features", outputCol="scaled_continuous_features")

# 8. Final feature vector
final_features = [
    "scaled_continuous_features", "MonthVec", "VisitorTypeVec", "WeekendVec",
    "Administrative", "Informational", "ProductRelated"
]

assembler_final = VectorAssembler(inputCols=final_features, outputCol="features")

# 9. Model
rf = RandomForestClassifier(featuresCol="features", labelCol="label", numTrees=100)

# 10. Pipeline
pipeline = Pipeline(stages=indexers + encoders + [assembler_continuous, scaler, assembler_final, rf])

# 11. Train-test split
train_df, _ = df.randomSplit([0.8, 0.2], seed=42)

# 12. Fit model
model = pipeline.fit(train_df)

# 13. Save model
model.save("model_rf")





