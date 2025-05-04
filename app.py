import streamlit as st
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("StreamlitOnlineShoppersIntention") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()

# Load trained model
model = PipelineModel.load("model_rf")

# App Title
st.title("🛍️ Online Shoppers Intention Predictor")

st.write("Please enter all the values as required below (match the dataset order):")

# Input fields in dataset column order (excluding dropped ones)
admin = st.text_input("Administrative")
admin_dur = st.text_input("Administrative_Duration")
info = st.text_input("Informational")
info_dur = st.text_input("Informational_Duration")
prod = st.text_input("ProductRelated")
prod_dur = st.text_input("ProductRelated_Duration")
bounce = st.text_input("BounceRates")
exit_r = st.text_input("ExitRates")
page_val = st.text_input("PageValues")
special_day = st.text_input("SpecialDay")
month = st.text_input("Month")  # e.g., "Nov"
visitor = st.text_input("VisitorType")  # e.g., "Returning_Visitor"
weekend = st.text_input("Weekend")  # e.g., "True" or "False"

if st.button("Predict"):
    # Validate all fields
    required_fields = [admin, admin_dur, info, info_dur, prod, prod_dur, bounce,
                       exit_r, page_val, special_day, month, visitor, weekend]

    if all(required_fields):
        try:
            # Prepare input
            input_data = [(month, visitor, weekend,
                           int(admin), int(info), int(prod),
                           float(admin_dur), float(info_dur), float(prod_dur),
                           float(bounce), float(exit_r), float(page_val), float(special_day))]

            columns = ["Month", "VisitorType", "Weekend", "Administrative", "Informational", "ProductRelated",
                       "Administrative_Duration", "Informational_Duration", "ProductRelated_Duration",
                       "BounceRates", "ExitRates", "PageValues", "SpecialDay"]

            df_input = spark.createDataFrame(input_data, columns)

            # Run prediction
            prediction = model.transform(df_input).select("prediction").collect()[0][0]

            if prediction == 1.0:
                st.success("✅ Will generate revenue")
            else:
                st.error("❌ Will not generate revenue")

        except ValueError:
            st.warning("⚠️ Please enter numeric values where required.")
    else:
        st.warning("⚠️ All fields are required.")
