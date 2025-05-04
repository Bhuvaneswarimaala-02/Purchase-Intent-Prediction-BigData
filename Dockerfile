# Base image with Java (required for Spark)
FROM openjdk:8-jdk-slim

# Set environment variables
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    wget \
    software-properties-common \
    && apt-get clean

# Install Python packages
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Install Spark
ENV SPARK_VERSION=3.3.1
ENV HADOOP_VERSION=3
RUN wget https://downloads.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar xvf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

ENV SPARK_HOME=/opt/spark
ENV PATH="$SPARK_HOME/bin:$PATH"

# Copy the app code
COPY . /app
WORKDIR /app

# Set the command to run your app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
