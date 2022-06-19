import os
import sys
from ast import literal_eval as make_tuple
from pyspark import SparkContext
#from pyspark import HiveContext



def extract_user(row):
    # if row is a string
    driverID = row.strip().split(',')[0]
    carPlateNumber = row.strip().split(',')[1]
    user = driverID + '+' + carPlateNumber
    # if you send a list, you could always extract the first item from that list as the domain name
    # domain = row[0]
    return user



def matrixSum(a, b):
    x = []
    for i in range(len(a)):
        x.append((a[i]) + (b[i]))
    return x
			
def extract_complex2(row):
    newrow = make_tuple(row)
    user = newrow[0]
    details = newrow[1]
    return (user, details)

args = sys.argv
inp = args[1]
out = args[2]

sc = SparkContext()
#sqlContext = HiveContext(sc)

text_file = sc.textFile(inp)
print("Readed")

# Add up the details of info
lines = text_file.flatMap(lambda line: line.split("\n")) \
            .map(lambda line: extract_complex2(line))


print("lines finished")
# a, b is each line in lines
counts = lines.reduceByKey(lambda a, b: matrixSum(a, b))

counts.repartition(1).saveAsTextFile(out)

#arr = counts.collect()
sc.stop()





