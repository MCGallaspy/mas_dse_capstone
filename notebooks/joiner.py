#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pyspark.sql import SparkSession
from pyspark.sql.window import Window
import pyspark.sql.functions as F
spark = SparkSession.builder.appName('GeoHashJoin').config("spark.driver.memory", "15g").getOrCreate()


# In[ ]:


weather_df = spark.read.parquet("s3a://dse-cohort5-group5/wildfire_capstone/integratedData/completePCA")
geomac_df = spark.read.parquet("s3://dse-cohort5-group5/wildfire_capstone/geoHashFires/geomac_with_lat_long.gz.parquet")


# In[ ]:


geomac_df = geomac_df.withColumn( "fire_date",F.from_unixtime(F.unix_timestamp('final_date', 'yyyy-MM-dd')).alias('date'))
geomac_df = geomac_df.withColumn("lat", F.col("latitude"))
geomac_df = geomac_df.withColumn("long", F.col("longitude"))
geomac_df = geomac_df.drop("latitude")
geomac_df = geomac_df.drop("longitude")

geomac_df.printSchema()

# In[ ]:


from pyspark.sql.functions import unix_timestamp, from_unixtime
joined_df = weather_df.join(geomac_df,  
                                    (geomac_df.lat == weather_df.latitude)& 
                                    (geomac_df.long == weather_df.longitude)& 
                                    (geomac_df.fire_date == weather_df.date),how='left')

joined_df = joined_df.coalesce(200)
joined_df.write.parquet("s3a://dse-cohort5-group5/wildfire_capstone/integratedData/completeWithFires",
                     mode="overwrite",
                     compression='gzip')

