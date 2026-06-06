# Machine learning model training for EMR PySpark pipeline

import subprocess

command = "pip install numpy"
subprocess.run(command.split())

import os
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
from upload_s3 import upload_ml_models


def train_evaluate_model(
    spark,
    classifier,
    features,
    classes,
    train,
    test,
    bucket,
    bucket_name,
    is_emr,
):
    """
    Trains a classifier and evaluates its accuracy.
    """

    def find_model_type(classifier):
        return type(classifier).__name__

    model_type = find_model_type(classifier)

    def fit_model(model_type, classifier, classes, features, train):
        if model_type in ("LogisticRegression"):
            # Hyperparameter grid for optimization
            paramGrid = (
                ParamGridBuilder().addGrid(classifier.maxIter, [10, 15, 20]).build()
            )

            # Cross-validation for hyperparameter tuning
            crossval = CrossValidator(
                estimator=classifier,
                estimatorParamMaps=paramGrid,
                evaluator=MulticlassClassificationEvaluator(),
                numFolds=2,
            )

            fitModel = crossval.fit(train)
            return fitModel

    # Train the model
    fitModel = fit_model(model_type, classifier, classes, features, train)

    # Print metrics
    if fitModel is not None:
        if model_type in ("LogisticRegression"):
            BestModel = fitModel.bestModel
            write_log(model_type, bucket)
            global LR_coefficients
            LR_coefficients = BestModel.coefficientMatrix.toArray()
            global LR_BestModel
            LR_BestModel = BestModel

    # Define result columns
    columns = ["Classifier", "Result"]

    # Generate predictions on test data
    predictions = fitModel.transform(test)

    # Create evaluator
    MC_evaluator = MulticlassClassificationEvaluator(metricName="accuracy")

    # Calculate accuracy
    accuracy = (MC_evaluator.evaluate(predictions)) * 100

    # Log results
    write_log("Classifier: " + model_type + " / Accuracy: " + str(accuracy), bucket)

    # Build result DataFrame
    model_type_list = [model_type]
    score = [str(accuracy)]
    result = spark.createDataFrame(zip(model_type_list, score), schema=columns)
    result = result.withColumn("Result", result.Result.substr(0, 5))

    # Paths for saving results
    path = (
        f"s3://{bucket_name}/output/" + model_type_list[0] + "_" + train.name
        if is_emr
        else "output/" + model_type_list[0] + "_" + train.name
    )
    s3_path = "output/" + model_type_list[0] + "_" + train.name

    # Upload model to S3
    upload_ml_models(fitModel, path, s3_path, bucket, is_emr)
    return result


def train_ml_models(
    spark,
    HTFfeaturizedData,
    TFIDFfeaturizedData,
    W2VfeaturizedData,
    bucket,
    bucket_name,
    is_emr,
):
    """
    Trains ML models across multiple feature sets.
    """

    # We use a single classifier, but more can be added
    classifiers = [LogisticRegression()]

    # Feature sets to iterate over
    featureDF_list = [HTFfeaturizedData, TFIDFfeaturizedData, W2VfeaturizedData]

    for featureDF in featureDF_list:
        write_log(featureDF.name + " Results: ", bucket)

        # Train/test split
        train, test = featureDF.randomSplit([0.7, 0.3], seed=11)

        # Feature set name
        train.name = featureDF.name

        # Features (input data)
        features = featureDF.select(["features"]).collect()

        # Classes (output labels)
        classes = featureDF.select("label").distinct().count()

        # Result schema
        columns = ["Classifier", "Result"]
        vals = [("Place Holder", "N/A")]
        results = spark.createDataFrame(vals, columns)

        for classifier in classifiers:
            new_result = train_evaluate_model(
                spark,
                classifier,
                features,
                classes,
                train,
                test,
                bucket,
                bucket_name,
                is_emr,
            )
            results = results.union(new_result)
            results = results.where("Classifier!='Place Holder'")
