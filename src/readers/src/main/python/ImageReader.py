# Copyright (C) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in project root for information.

import sys

if sys.version >= '3':
    basestring = str

import pyspark
from pyspark import SparkContext
from pyspark import sql
from pyspark.ml.param.shared import *
from pyspark.sql import DataFrame

def readImages(sparkSession, path, recursive = False, sampleRatio = 1.0, inspectZip = True):
    """
    Reads the directory of images from the local or remote (WASB) source.
    This function is attached to SparkSession class.
    Example: spark.readImages(path, recursive, ...)

    Args:
        sparkSession (SparkSession): Existing sparkSession
        path (str): Path to the image directory
        recursive (bool): Recursive search flag
        sampleRatio (double): Fraction of the images loaded

    Returns:
        DataFrame: DataFrame with a single column of "images", see imageSchema for details
    """
    ctx = SparkContext.getOrCreate()
    reader = ctx._jvm.com.microsoft.ml.spark.ImageReader
    sql_ctx = pyspark.SQLContext.getOrCreate(ctx)
    jsession = sql_ctx.sparkSession._jsparkSession
    jresult = reader.read(path, recursive, jsession, float(sampleRatio), inspectZip)
    return DataFrame(jresult, sql_ctx)

setattr(sql.SparkSession, 'readImages', classmethod(readImages))

def isImage(df, column):
    """
    Returns True if the column contains images

    Args:
        df (DataFrame): The DataFrame to be processed
        column  (str): The name of the column being inspected

    Returns:
        bool: True if the colum is an image column
    """

    jvm = SparkContext.getOrCreate()._jvm
    schema = jvm.com.microsoft.ml.spark.schema.ImageSchema
    return schema.isImage(df._jdf, column)
