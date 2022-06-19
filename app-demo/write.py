import time
import json
from os import listdir
from os.path import isfile, join
from db_conn import db_connection

def getFileList(path):
    recordsPath = path
    files = listdir(recordsPath)
    fileList = []

    for f in files:
        fullpath = join(recordsPath, f)
        if isfile(fullpath):
            #print("File: ", f)
            fileList.append(fullpath)

    return fileList

fileList = getFileList(f'detail-records')

nameOfKeys = ['driverID', 'carPlateNumber', 'Latitude',
    'Longtitude',
    'Speed',
    'Direction',
    'siteName',
    'time',
    'isRapidlySpeedup',
    'isRapidlySlowdown',
    'isNeutralSlide',
    'isNeutralSlideFinished',
    'NeutralSlide',
    'isOverspeed',
    'isOverspeedFinished',
    'overspeedTime',
    'isFatigueDriving',
    'isHthrottleStop',
    'isOilLeak'
    ]


mydb = db_connection()
cur = mydb.cursor()

def dataReformat(l):
    Time = int(time.time())
    data = {}

    #print(len(l))
    if len(l) == 8:
        #print("short l")
        isShort = True
    elif len(l) == 20:
        #print("long l")
        isShort = False
    else:
        isShort = False
        print("Something wrong with the length of data in l")

    for i in range(19):
        if isShort and i > 7:
            data[nameOfKeys[i]] = 'NULL'
            continue
        if nameOfKeys[i] == 'time':
            data[nameOfKeys[i]] = Time
        else:
            #print(l[i])
            try:
                data[nameOfKeys[i]] = float(l[i])
            except ValueError:
                if l[i] == '':
                    data[nameOfKeys[i]] = 'NULL'
                else: 
                    data[nameOfKeys[i]] = l[i]
    
    #print("data after reformat")
    #print(data)

    return data

    


def readRaw(f):
    with open(f, encoding='utf-8') as file:
        lines = file.readlines()
    return lines

insertCols = ['driverID', 
    'carPlateNumber',
    'Speed',
    'time',
    'isRapidlySpeedup',
    'isRapidlySlowdown',
    'isOverspeed',
    'isOverspeedFinished']

def genSQL(d):
    #print(d)
    sql_start = "insert into drivingRecord values ("
    sql_end =")"
    sql_data = ""
    for key, value in d.items():
        if key in insertCols:
            try:
                sql_data = sql_data + '\'' + str(value) + '\'' +','
            except:
                sql_data = sql_data + '\'' +str(value) + '\'' +','
    
    sql_data = sql_data[:-1] # remove tailing comma
    sql3 = sql_start + sql_data + sql_end

    #print(sql3)
    return sql3


def execute():
    for f in fileList:
        print(f"Handling: {f}")
        lines = readRaw(f)
        for line in lines:
            lineSlist = line.split(',')
            #print(f'datalist:\n{lineSlist}')
            
            data = dataReformat(lineSlist)
            
            #print((data['driverID'][0]))
            sql = genSQL(data)
            #print(sql)
            
            #return
            ret = cur.execute(sql) # run sql
            print("Inserted...")
            #time.sleep(0.001)
        #return

if __name__ == "__main__":
    while True:   
        execute()
        time.sleep(1)
        #break