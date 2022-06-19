import pyspark.sql.types as t
from pyspark import SparkContext
from pyspark.sql import SparkSession

schema = t.StructType([
    t.StructField('driverID', t.StringType(), False),
    t.StructField('carPlateNumber', t.StringType(), False),
    t.StructField('Latitude', t.DoubleType(), False),
    t.StructField('Longtitude', t.DoubleType(), False),
    t.StructField('Speed', t.IntegerType(), False),
    t.StructField('Direction', t.IntegerType(), True),
    t.StructField('siteName', t.StringType(), True),
    t.StructField('Time', t.TimestampType(), False),
    t.StructField('isRapidlySpeedup', t.ByteType(), True),
    t.StructField('isRapidlySlowdown', t.ByteType(), True),
    t.StructField('isNeutralSlide', t.ByteType(), True),
    t.StructField('isNeutralSlideFinished', t.ByteType(), True),
    t.StructField('neutralSlideTime', t.IntegerType(), True),
    t.StructField('isOverspeed', t.ByteType(), True),
    t.StructField('isOverspeedFinished', t.ByteType(), True),
    t.StructField('overspeedTime', t.IntegerType(), True),
    t.StructField('isFatigueDriving', t.ByteType(), True),
    t.StructField('isHthrottleStop', t.ByteType(), True),
    t.StructField('isOilLeak', t.ByteType(), True),
])

if not spark:
    spark = SparkSession.builder.master("local[*]").getOrCreate()
sc = SparkContext.getOrCreate()

args = sys.argv

# should be a source bucket like s3://comp4442-project/detail-records
inp = args[1]

# should be a sink bucket like s3://comp4442-project/records-processed
out = args[2]

df = spark.read.csv(inp, schema=schema)
df.createOrReplaceTempView("records")

def dump_summary():
    return spark.sql("""
        SELECT CONCAT(driverID, "+", carPlateNumber),
            COUNT(isRapidlySpeedup = 1),
            COUNT(isRapidlySlowdown = 1),
            COUNT(isNeutralSlide = 1),
            COUNT(isNeutralSlideFinished = 1),
            SUM(neutralslideTime),
            COUNT(isOverspeed = 1),
            COUNT(isOverspeedFinished = 1),
            SUM(overspeedTime),
            COUNT(isFatigueDriving = 1),
            COUNT(isHthrottleStop = 1),
            COUNT(isOilLeak = 1)
        FROM records
        GROUP BY driverID, carPlateNumber
    """)

def dump_driver_data_by_date(day: int):
    return spark.sql(f"""
        SELECT CONCAT(driverID, "+", carPlateNumber),
            COUNT(isRapidlySpeedup = 1),
            COUNT(isRapidlySlowdown = 1),
            COUNT(isNeutralSlide = 1),
            COUNT(isNeutralSlideFinished = 1),
            SUM(neutralslideTime),
            COUNT(isOverspeed = 1),
            COUNT(isOverspeedFinished = 1),
            SUM(overspeedTime),
            COUNT(isFatigueDriving = 1),
            COUNT(isHthrottleStop = 1),
            COUNT(isOilLeak = 1)
        FROM records
        WHERE to_date(time, "yyyy/mm/dd") = '2017-01-{day}'
        GROUP BY driverID, carPlateNumber
    """)

summary = dump_summary()
summary.rdd.repartition(1).map(lambda x: (x[0], list(x[1:]))).saveAsTextFile(f"{out}/summary")

for day in range(1, 11 + 1):
    data = dump_driver_data_by_date(day)
    data.rdd.repartition(1).map(lambda x: (x[0], list(x[1:]))).saveAsTextFile(f"{out}/day{str(day).zfill(2)}")