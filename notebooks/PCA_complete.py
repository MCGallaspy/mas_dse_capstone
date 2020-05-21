#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pyspark.sql import SparkSession
from pyspark.sql.window import Window
import pyspark.sql.functions as F
spark = SparkSession.builder.appName('PCA').getOrCreate()
df = spark.read.parquet('s3://dse-cohort5-group5/wildfire_capstone/completeWeatherTestFullR3/*')


# In[ ]:


c = df.schema.names
c = [x for x in c if x != "date" and x != "longitude" and x!= "latitude" and x!= "cumLag" and "lag-" not in x]


# In[ ]:


from pyspark.ml.feature import VectorAssembler, StandardScaler
assembler = VectorAssembler(inputCols=c, outputCol="features")
scaler = StandardScaler(inputCol="features", outputCol="scaledFeatures", withStd=True, withMean=True)
df1 = assembler.setHandleInvalid("skip").transform(df)
df1.printSchema()
print("df1 count at this point is ", df1.count())
scalarModel = scaler.fit(df1)
df1 = scalarModel.transform(df1)
from pyspark.ml.feature import PCA
pca = PCA(k=40, inputCol="scaledFeatures", outputCol="pcaFeatures")
model = pca.fit(df1)
result = model.transform(df1)    .select('date', 'latitude', 'longitude', 'pcaFeatures')


# In[ ]:

result = result.coalesce(200)
result.write.parquet("s3a://dse-cohort5-group5/wildfire_capstone/integratedData/completePCA",
                     mode="overwrite",
                     compression='gzip')

