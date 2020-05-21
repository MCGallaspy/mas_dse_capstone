from pyspark.sql import SparkSession
from pyspark.sql.window import Window
import pyspark.sql.functions as F
spark = SparkSession.builder.appName('DeadFuelLag').config("spark.executor.instances", 200)\
.getOrCreate()


s3_url = 's3a://dse-cohort5-group5/wildfire_capstone/completeWeatherTestFullR2/*'

df = spark.read.parquet(s3_url)
# for c in df.columns:
#     df = df.withColumnRenamed(c, c.replace(" ", ""))

#df = spark.read.schema(df.schema).parquet(s3_url)

df = df.where(F.col("precipitation_amount_mm").isNotNull())

# geomac_df = spark.read.parquet("s3a://dse-cohort5-group5/wildfire_capstone/GeomacHashesV2.parquet")



df.printSchema()

from pyspark.sql.functions import udf
from pyspark.sql.types import LongType, StringType


# @udf("string")
# def geohash_point(lat ,long):
#     import Geohash
#     return Geohash.encode(lat, long, precision=5)
# weather_df = df.withColumn("geohash", geohash_point(F.col("latitude"), F.col("longitude")))
# #geomac_df = geomac_df.withColumnRenamed("fire_date", "date")
# geomac_ex = geomac_df.withColumn("geohash_mac", F.explode("hashes"))
# df = weather_df.join(geomac_ex, (geomac_ex.fire_date == weather_df.date) & (geomac_ex.geohash_mac == weather_df.geohash),how='left')



windowSpec = Window.partitionBy(F.col("latitude"), F.col("longitude")).orderBy(F.col("date").asc())
df = df.withColumn("cumLag", F.lit(0))
for i in range(1,8):
    df = df.withColumn("lag-"+str(i),F.col("dead_fuel_moisture_1000hr_Percent")- F.lag(F.col("dead_fuel_moisture_1000hr_Percent"), i).over(windowSpec))
    df = df.withColumn("cumLag", F.when((F.col("lag-"+str(i))<= 0) & (F.col("cumLag") == i-1), i ).otherwise(F.col("cumLag")))





def AggFunctions(df, cols):

    org_window = Window.partitionBy(F.col("latitude"), F.col("longitude")).orderBy(F.col("date").asc())
    windowSpec = org_window.rowsBetween(-7,0)
    for idx, col in enumerate(cols):
        df = df.withColumn(col+"_mean_7_days", F.avg(F.col(col)).over(windowSpec))
        df = df.withColumn(col+"_max_7_days", F.max(F.col(col)).over(windowSpec.rowsBetween(-7,0)))
        df = df.withColumn(col+"_min_7_days", F.min(F.col(col)).over(windowSpec.rowsBetween(-7,0)))
        df = df.withColumn(col+"_cummalitive_7_days", F.sum(F.col(col)).over(windowSpec.rowsBetween(-7,0)))
        df = df.withColumn(col+"_std_7_days", F.stddev(F.col(col)).over(windowSpec.rowsBetween(-7,0)))

    windowSpec = org_window.rowsBetween(-14,0)
    for idx, col in enumerate(cols):   
        df = df.withColumn(col+"_mean_14_days", F.avg(F.col(col)).over(windowSpec.rowsBetween(-14,0)))
        df = df.withColumn(col+"_max_14_days", F.max(F.col(col)).over(windowSpec.rowsBetween(-14,0)))
        df = df.withColumn(col+"_min_14_days", F.min(F.col(col)).over(windowSpec.rowsBetween(-14,0)))
        df = df.withColumn(col+"_cummalitive_14_days", F.sum(F.col(col)).over(windowSpec.rowsBetween(-14,0)))
        df = df.withColumn(col+"_std_14_days", F.stddev(F.col(col)).over(windowSpec.rowsBetween(-14,0)))

    windowSpec = org_window.rowsBetween(-30,0)
    for idx, col in enumerate(cols):
        df = df.withColumn(col+"_mean_30_days", F.avg(F.col(col)).over(windowSpec.rowsBetween(-30,0)))
        df = df.withColumn(col+"_max_30_days", F.max(F.col(col)).over(windowSpec.rowsBetween(-30,0)))
        df = df.withColumn(col+"_min_30_days", F.min(F.col(col)).over(windowSpec.rowsBetween(-30,0)))
        df = df.withColumn(col+"_cummalitive_30_days", F.sum(F.col(col)).over(windowSpec.rowsBetween(-30,0)))
        df = df.withColumn(col+"_std_30_days", F.stddev(F.col(col)).over(windowSpec.rowsBetween(-30,0)))

    windowSpec = org_window.rowsBetween(-60,0)
    for idx, col in enumerate(cols):
        df = df.withColumn(col+"_mean_60_days", F.avg(F.col(col)).over(windowSpec.rowsBetween(-60,0)))
        df = df.withColumn(col+"_max_60_days", F.max(F.col(col)).over(windowSpec.rowsBetween(-60,0)))
        df = df.withColumn(col+"_min_60_days", F.min(F.col(col)).over(windowSpec.rowsBetween(-60,0)))
        df = df.withColumn(col+"_cummalitive_60_days", F.sum(F.col(col)).over(windowSpec.rowsBetween(-60,0)))
        df = df.withColumn(col+"_std_60_days", F.stddev(F.col(col)).over(windowSpec.rowsBetween(-60,0)))
    
    windowSpec = org_window.rowsBetween(-90,0)
    for idx, col in enumerate(cols):
        df = df.withColumn(col+"_mean_90_days", F.avg(F.col(col)).over(windowSpec.rowsBetween(-90,0)))
        df = df.withColumn(col+"_max_90_days", F.max(F.col(col)).over(windowSpec.rowsBetween(-90,0)))
        df = df.withColumn(col+"_min_90_days", F.min(F.col(col)).over(windowSpec.rowsBetween(-90,0)))
        df = df.withColumn(col+"_cummalitive_90_days", F.sum(F.col(col)).over(windowSpec.rowsBetween(-90,0)))
        df = df.withColumn(col+"_std_90_days", F.stddev(F.col(col)).over(windowSpec.rowsBetween(-90,0)))

    windowSpec = org_window.rowsBetween(-180,0)
    for idx, col in enumerate(cols):
        df = df.withColumn(col+"_mean_6_months", F.avg(F.col(col)).over(windowSpec.rowsBetween(-180,0)))
        df = df.withColumn(col+"_max_6_months", F.max(F.col(col)).over(windowSpec.rowsBetween(-180,0)))
        df = df.withColumn(col+"_min_6_months", F.min(F.col(col)).over(windowSpec.rowsBetween(-180,0)))
        df = df.withColumn(col+"_cummalitive_6_months", F.sum(F.col(col)).over(windowSpec.rowsBetween(-180,0)))
        df = df.withColumn(col+"_std_6_months", F.stddev(F.col(col)).over(windowSpec.rowsBetween(-180,0)))

    windowSpec = org_window.rowsBetween(-365,0)
    for idx, col in enumerate(cols):
        df = df.withColumn(col+"_mean_1_year", F.avg(F.col(col)).over(windowSpec.rowsBetween(-365,0)))
        df = df.withColumn(col+"_max_1_year", F.max(F.col(col)).over(windowSpec.rowsBetween(-365,0)))       
        df = df.withColumn(col+"_min_1_year", F.min(F.col(col)).over(windowSpec.rowsBetween(-365,0)))     
        df = df.withColumn(col+"_cummalitive_1_year", F.sum(F.col(col)).over(windowSpec.rowsBetween(-365,0)))
        df = df.withColumn(col+"_std_1_year", F.stddev(F.col(col)).over(windowSpec.rowsBetween(-365,0)))
    return df
        
agg_cols = ['precipitation_amount_mm',
'relative_humidity_%',
'specific_humidity_kg/kg',
'wind_speed_m/s',
'max_air_temperature_K',
# 'min_air_temperature_K',
# 'burning_index_g_Unitless',
# 'dead_fuel_moisture_100hr_Percent',
# 'dead_fuel_moisture_1000hr_Percent',
# 'energy_release_component-g_Unitless',
# 'potential_evapotranspiration_mm',
# 'mean_vapor_pressure_deficit_kPa',
# 'surface_downwelling_shortwave_flux_in_air_Wm-2',
# 'wind_from_direction_DegreesClockwisefromnorth'
]
df = AggFunctions(df,agg_cols)
        




#df = df.withColumn("movingAvg",F.avg(F.col("dead_fuel_moisture_1000hr_Percent")).over(windowSpec.rowsBetween(-7,0)))





        




# from pyspark.ml.feature import OneHotEncoderEstimator, StringIndexer, VectorAssembler
# from pyspark.ml.classification import LogisticRegression





df.write.parquet("s3a://dse-cohort5-group5/wildfire_capstone/completeWeatherTestFullR3",
                     mode="overwrite",
                     compression='gzip')




