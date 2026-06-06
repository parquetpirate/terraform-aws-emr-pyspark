# Data cleaning and feature engineering for EMR PySpark pipeline

import os
import os.path
import numpy
from pyspark.ml.feature import *
from pyspark.sql import functions
from pyspark.sql.functions import *
from pyspark.sql.types import StringType, IntegerType
from pyspark.ml.classification import *
from pyspark.ml.evaluation import *
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import StopWordsRemover
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from log import write_log
from upload_s3 import upload_processed_data


def calculate_null_values(df):
    """
    Calculates the count and percentage of null values for each column in a DataFrame.
    """

    null_columns_counts = []
    numRows = df.count()

    for k in df.columns:
        nullRows = df.where(col(k).isNull()).count()
        if nullRows > 0:
            temp = k, nullRows, (nullRows / numRows) * 100
            null_columns_counts.append(temp)

    return null_columns_counts


def clean_transform_data(spark, bucket, bucket_name, is_emr):
    """
    Cleans and transforms the raw dataset into feature-ready DataFrames.
    """

    # Determine storage path
    path = f"s3://{bucket_name}/data/" if is_emr else "data/"

    write_log("Log - Importing data...", bucket)

    # Load CSV file
    reviews = spark.read.csv(path + "dataset.csv", header=True, escape='"')

    write_log("Log - Data imported successfully.", bucket)
    write_log("Log - Total records: " + str(reviews.count()), bucket)
    write_log("Log - Checking for null values.", bucket)

    # Calculate missing values
    null_columns_calc_list = calculate_null_values(reviews)

    # Handle missing values
    if len(null_columns_calc_list) > 0:
        for column in null_columns_calc_list:
            write_log(
                "Column "
                + str(column[0])
                + " has "
                + str(column[2])
                + "% null data",
                bucket,
            )
        reviews = reviews.dropna()
        write_log("Null data dropped.", bucket)
        write_log(
            "Log - Total records after cleaning: " + str(reviews.count()),
            bucket,
        )
    else:
        write_log("Log - No missing values detected.", bucket)

    write_log("Log - Checking class balance.", bucket)

    # Count positive and negative reviews
    count_positive_sentiment = reviews.where(reviews["sentiment"] == "positive").count()
    count_negative_sentiment = reviews.where(reviews["sentiment"] == "negative").count()

    write_log(
        "Log - There are "
        + str(count_positive_sentiment)
        + " positive reviews and "
        + str(count_negative_sentiment)
        + " negative reviews.",
        bucket,
    )

    df = reviews

    write_log("Log - Transforming data.", bucket)

    # Index sentiment labels
    indexer = StringIndexer(inputCol="sentiment", outputCol="label")
    df = indexer.fit(df).transform(df)

    write_log("Log - Cleaning text data.", bucket)

    # Remove special characters from text
    df = df.withColumn("review", regexp_replace(df["review"], "<.*/>", ""))
    df = df.withColumn("review", regexp_replace(df["review"], "[^A-Za-z ]+", ""))
    df = df.withColumn("review", regexp_replace(df["review"], " +", " "))
    df = df.withColumn("review", lower(df["review"]))

    write_log("Log - Text data cleaned.", bucket)
    write_log("Log - Tokenizing text data.", bucket)

    # Tokenize text into words
    regex_tokenizer = RegexTokenizer(
        inputCol="review", outputCol="words", pattern="\\W"
    )
    df = regex_tokenizer.transform(df)

    write_log("Log - Removing stop words.", bucket)

    # Remove stop words
    remover = StopWordsRemover(inputCol="words", outputCol="filtered")
    feature_data = remover.transform(df)

    write_log("Log - Applying HashingTF.", bucket)

    # HashingTF feature extraction
    hashingTF = HashingTF(inputCol="filtered", outputCol="rawfeatures", numFeatures=250)
    HTFfeaturizedData = hashingTF.transform(feature_data)

    write_log("Log - Applying IDF.", bucket)

    # IDF transformation
    idf = IDF(inputCol="rawfeatures", outputCol="features")
    idfModel = idf.fit(HTFfeaturizedData)
    TFIDFfeaturizedData = idfModel.transform(HTFfeaturizedData)

    # Set feature names
    TFIDFfeaturizedData.name = "TFIDFfeaturizedData"
    HTFfeaturizedData = HTFfeaturizedData.withColumnRenamed("rawfeatures", "features")
    HTFfeaturizedData.name = "HTFfeaturizedData"

    write_log("Log - Applying Word2Vec.", bucket)

    # Word2Vec feature extraction
    word2Vec = Word2Vec(
        vectorSize=250, minCount=5, inputCol="filtered", outputCol="features"
    )
    model = word2Vec.fit(feature_data)
    W2VfeaturizedData = model.transform(feature_data)

    write_log("Log - Scaling with MinMaxScaler.", bucket)

    # MinMax scaling
    scaler = MinMaxScaler(inputCol="features", outputCol="scaledFeatures")
    scalerModel = scaler.fit(W2VfeaturizedData)
    scaled_data = scalerModel.transform(W2VfeaturizedData)

    # Rename scaled features
    W2VfeaturizedData = scaled_data.select(
        "sentiment", "review", "label", "scaledFeatures"
    )
    W2VfeaturizedData = W2VfeaturizedData.withColumnRenamed(
        "scaledFeatures", "features"
    )
    W2VfeaturizedData.name = "W2VfeaturizedData"

    write_log("Log - Saving cleaned and transformed data.", bucket)

    # Upload processed data to S3
    path = f"s3://{bucket_name}/data/" if is_emr else "data/"
    s3_path = "data/"

    upload_processed_data(
        HTFfeaturizedData,
        path + "HTFfeaturizedData",
        s3_path + "HTFfeaturizedData",
        bucket,
        is_emr,
    )
    upload_processed_data(
        TFIDFfeaturizedData,
        path + "TFIDFfeaturizedData",
        s3_path + "TFIDFfeaturizedData",
        bucket,
        is_emr,
    )
    upload_processed_data(
        W2VfeaturizedData,
        path + "W2VfeaturizedData",
        s3_path + "W2VfeaturizedData",
        bucket,
        is_emr,
    )

    return HTFfeaturizedData, TFIDFfeaturizedData, W2VfeaturizedData
