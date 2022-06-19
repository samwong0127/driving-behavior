import os
import sys
from os import listdir
from os.path import isfile, join

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

def extract_tailing_info(row):
    print('handling:')
    record = row.strip().split(',')
    print(f"length of record: {len(record)}")
    print(record)

    if len(record) < 19:
		# Short record
        return [0]*11
    else:
        output = []
		# Long record
        record = record[8:-1]
        print(record)
        if len(record) != 11:
            print('something wrong')
        for i in range(11):
            if record[i] == '':
                output.append(0)
            else:
                output.append(float(record[i]))
            
        return output			
			
def extract_complex(row):
	user = extract_user(row)
	details = extract_tailing_info(row)
	
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
            .map(lambda line: extract_complex(line))


print("lines finished")
# a, b is each line in lines
counts = lines.reduceByKey(lambda a, b: matrixSum(a, b))

counts.repartition(1).saveAsTextFile(out)

#arr = counts.collect()
    
sc.stop()





