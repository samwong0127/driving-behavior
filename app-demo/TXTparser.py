from ast import literal_eval as make_tuple
import glob
from os import getenv
from os.path import abspath, sep


def readRaw(f):
    with open(f, encoding='utf-8') as file:
        lines = file.readlines()
    return lines


def getFileList(path):
    return [abspath(x) for x in glob.iglob(f"{path}/**/part-00000", recursive=True)]


filelist = getFileList(getenv("PROCESSED_FILE_LOCATION", f'detail-records/summary/processed'))


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
        # print(type(x))
        # print(x)
        driverID = x[0].split('+')[0]
        carPlateNumber = x[0].split('+')[1]
        cumOverSpeed = x[1][5]
        cumFatigue = x[1][8]
        totalOverSpeed = x[1][7]
        totalNeutralSlide = x[1][4]

        results.append([driverID, carPlateNumber, cumOverSpeed,
                       cumFatigue, totalOverSpeed, totalNeutralSlide])

    return results

# Return a 2d array: [[details of driver 1], [details of driver 2], ...]


def getSummary():
    for f in filelist:
        if 'summary' in list(reversed(f.split(sep)))[1]:
            lines = readRaw(f)
            results = gen2darray(lines)
            # print(results)
            return results

# Return a dict: {'10 Jan':[[details of driver 1], [details of driver 2], ...], ...}


def getSummaryByDay():
    resultsByDay = {}
    for f in filelist:
        name = list(reversed(f.split(sep)))[1]
        if 'day' in name:
            day = int(name[3:]) 
            lines = readRaw(f)
            results = gen2darray(lines)
            # print(results)
            resultsByDay[f'{day} Jan'] = results

    return resultsByDay

# print(getSummaryByDay())
