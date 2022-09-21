# Databricks notebook source
# Import packages
# Pyspark
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import IntegerType
from pyspark.sql.types import DateType
from pyspark.sql.types import DecimalType
from pyspark.sql.types import StringType
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml import Pipeline
from pyspark.sql import functions as F
from pyspark.sql.types import (
    IntegerType,
    DateType,
    FloatType,
    StringType,
    TimestampType 
)


# EDA
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime

# COMMAND ----------

# Instantiate a local SparkSession() and save the results in a variable called spark
spark = (
    SparkSession
    .builder
    .appName('new_york_taxis')
    .getOrCreate()
)

# COMMAND ----------

# Create 3 variables:
storage_account_name = "utsbdeleah"
storage_account_access_key = "DP6nrm1xxzxdtulPzAC8P2dtX9ElEaaPu0Tm6+h+rD7iIkgqUajq/Gk7VlaB4XOqjSeJxPGaIzYo+AStN3yBlw=="
blob_container_name = "animal-logic-sample"

# COMMAND ----------

# Mount the blob container into the Databricks Files System:
dbutils.fs.mount(
  source = f'wasbs://{blob_container_name}@{storage_account_name}.blob.core.windows.net',
  mount_point = f'/mnt/{blob_container_name}/',
  extra_configs = {'fs.azure.account.key.' + storage_account_name + '.blob.core.windows.net': storage_account_access_key}
)

# COMMAND ----------

# List files inside Azure blob container
dbutils.fs.ls("/mnt/animal-logic-sample/")

# COMMAND ----------

df_dict = {}
file_type = ['timesheets', 'versions']

# create a loop that read all colour data by parsing file pattern
for file in file_type:
    path = f'/mnt/animal-logic-sample/{file}-*.csv'
    df = spark.read.option("header", True).csv(path)
    
    # Add the taxi colour
    df = df.withColumn('file', F.lit(file))
    df_dict[file] = df

# df contain all yellow taxi data
timesheets_df = df_dict['timesheets'] 
# df contain all green taxi data
versions_df = df_dict['versions']

# COMMAND ----------

csv_file = spark.read.option("header", True).csv("/mnt/animal-logic-sample/productivity.csv")
display(csv_file)
csv_file.write.parquet('/mnt/animal-logic-sample/productivity', mode='overwrite')

# COMMAND ----------

df = spark.read.option("header", True).parquet("/mnt/animal-logic-sample/productivity")
df.display()
