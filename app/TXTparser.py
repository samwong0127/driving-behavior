import json
from write import readRaw, getFileList
from ast import literal_eval as make_tuple
import re

filelist = getFileList(f'detail-records/summary')


nameOfKeys2 = [
    'isRapidlySpeedup',
    'isRapidlySlowdown',
    'isNeutralSlide',
    'isNeutralSlideFinished',
    'neutralslideTime',
    'isOverspeed',
    'isOverspeedFinished',
    'overspeedTime',
    'isFatigueDriving',
    'isHthrottleStop',
    'isOilLeak'
]


def gen2darray(lines):
    results = []
    for line in lines:
        x = make_tuple(line)
        #print(type(x))
        #print(x)
        driverID = x[0].split('+')[0]
        carPlateNumber = x[0].split('+')[1]
        cumOverSpeed = x[1][5]
        cumFatigue = x[1][8]
        totalOverSpeed = x[1][7]
        totalNeutralSlide = x[1][4]

        results.append([driverID, carPlateNumber, cumOverSpeed, cumFatigue, totalOverSpeed, totalNeutralSlide])

    return results

# Return a 2d array: [[details of driver 1], [details of driver 2], ...]
def getSummary():
    for f in filelist:
        #print(f"Handling: {f}")
        if 'summary-part' in f:
            lines = readRaw(f)
            results = gen2darray(lines)
            #print(results)
            return results

# Return a dict: {'10 Jan':[[details of driver 1], [details of driver 2], ...], ...}
def getSummaryByDay():
    resultsByDay = {}
    for f in filelist:
        if 'summary-part' not in f:
            #print(f"Handling: {f}")
            day = re.split(r'-|\\|\/', f)[3][:-1]
            if int(day) < 20:
                day = day[1] + ' Jan'
            else:
                day = day[1:] + ' Jan'
            #print(day)
            lines = readRaw(f)
            results = gen2darray(lines)
            #print(results)
            resultsByDay[day] = results
    
    return resultsByDay


#print(getSummaryByDay())