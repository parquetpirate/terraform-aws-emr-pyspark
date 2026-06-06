# Machine learning model training for EMR PySpark pipeline

from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from log import write_log
from upload_s3 import upload_ml_models


def train_evaluate_model(
    spark,
    classifier,
    train,
    test,
    bucket,
    bucket_name,
    is_emr,
):
    """
    Trains a classifier and evaluates its accuracy.
    """

    model_type = type(classifier).__name__

    if model_type == "LogisticRegression":
        paramGrid = (
            ParamGridBuilder().addGrid(classifier.maxIter, [10, 15, 20]).build()
        )
        crossval = CrossValidator(
            estimator=classifier,
            estimatorParamMaps=paramGrid,
            evaluator=MulticlassClassificationEvaluator(),
            numFolds=2,
        )
        fitModel = crossval.fit(train)
    else:
        raise ValueError(f"Unsupported classifier type: {model_type}")

    write_log(model_type, bucket)

    # Define result columns
    columns = ["Classifier", "Result"]

    # Generate predictions on test data
    predictions = fitModel.transform(test)

    # Create evaluator
    MC_evaluator = MulticlassClassificationEvaluator(metricName="accuracy")

    # Calculate accuracy
    accuracy = (MC_evaluator.evaluate(predictions)) * 100

    # Log results
    write_log(f"Classifier: {model_type} / Accuracy: {accuracy}", bucket)

    # Build result DataFrame
    score = [str(accuracy)]
    result = spark.createDataFrame(zip([model_type], score), schema=columns)
    result = result.withColumn("Result", result.Result.substr(0, 5))

    # Paths for saving results
    path = (
        f"s3://{bucket_name}/output/{model_type}_{train.name}"
        if is_emr
        else f"output/{model_type}_{train.name}"
    )
    s3_path = f"output/{model_type}_{train.name}"

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

    classifiers = [LogisticRegression()]

    featureDF_list = [HTFfeaturizedData, TFIDFfeaturizedData, W2VfeaturizedData]

    for featureDF in featureDF_list:
        write_log(featureDF.name + " Results: ", bucket)

        # Train/test split
        train, test = featureDF.randomSplit([0.7, 0.3], seed=11)

        # Feature set name
        train.name = featureDF.name

        # Result schema
        columns = ["Classifier", "Result"]
        vals = [("Place Holder", "N/A")]
        results = spark.createDataFrame(vals, columns)

        for classifier in classifiers:
            new_result = train_evaluate_model(
                spark,
                classifier,
                train,
                test,
                bucket,
                bucket_name,
                is_emr,
            )
            results = results.union(new_result)
            results = results.where("Classifier!='Place Holder'")
