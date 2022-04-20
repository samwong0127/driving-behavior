import time
import json
from os import listdir
from os.path import isfile, join
from db_conn import db_connection


recordsPath = f'detail-records/'
files = listdir(recordsPath)
fileList = []

for f in files:
  fullpath = join(recordsPath, f)
  if isfile(fullpath):
    print("檔案：", f)
    fileList.append(fullpath)

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
    'isNeutralSlide',
    'isOverspeed',
    'isOverspeedFinished',
    'overspeedTime',
    'isFatigueDriving',
    'isHthrottleStop',
    'isOilLeak'
    ]


#mydb = db_connection()
#cur = mydb.cursor()

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

    """
    #print((l[0]))
    data['driverID'] = l[0],
    data['carPlateNumber'] = l[1],
    data['Latitude'] = float(l[2]),
    data['Longtitude'] = float(l[3]),
    data['Speed'] = float(l[4]),
    data['Direction'] = float(l[5]),
    data['siteName'] = l[6],
    data['time'] = Time
    data['isRapidlySpeedup'] = l[8],
    data['isRapidlySlowdown'] = l[9],
    data['isNeutralSlide'] = l[10],
    data['isNeutralSlideFinished'] = l[11],
    data['neutralSlideTime'] = l[12],
    data['isOverspeed'] = l[13],
    data['isOverspeedFinished'] = l[14],
    data['overspeedTime'] = l[15],
    data['isFatigueDriving'] = l[16],
    data['isHthrottleStop'] = l[17],
    data['isOilLeak'] = l[18]
    
    #print(data)
    return data
    """


def readRaw(f):
    with open(f, encoding='utf-8') as file:
        lines = file.readlines()
    return lines

def genSQL(d):
    #print(d)
    """
    sql = "insert into drivingRecord values ({0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18})".format(
        d['driverID'][0],
        d['carPlateNumber'][0],
        d['Latitude'][0] ,
        d['Longtitude'][0] ,
        d['Speed'][0] ,
        d['Direction'][0] ,
        d['siteName'][0] ,
        d['time'],
        d['isRapidlySpeedup'][0],
        d['isRapidlySlowdown'][0] ,
        d['isNeutralSlide'][0] ,
        d['isNeutralSlideFinished'][0] ,
        d['neutralSlideTime'][0] ,
        d['isOverspeed'][0] ,
        d['isOverspeedFinished'][0] ,
        d['overspeedTime'][0] ,
        d['isFatigueDriving'][0],
        d['isHthrottleStop'][0],
        d['isOilLeak'][0]     
    )
    """

    
    sql_start = "insert into drivingRecord values ("
    sql_end =")"
    sql_data = ""
    for value in d.values():
        try:
            sql_data = sql_data + str(value) + ','
        except:
            sql_data = sql_data + str(value) + ','
    
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
            print(sql)
            
            return
            
            #ret = cur.execute(sql) # run sql
        return

if __name__ == "__main__":
    while True:   
        execute()
        #time.sleep(1)
        break