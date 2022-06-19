from os import listdir
from os.path import isfile, join

dirs = listdir(f'summary')
files = []
for f in dirs:
    fullpath = join('summary/', f)
    if isfile(fullpath):
        print("File: ", f)
        files.append(fullpath)

def readRaw(f):
    with open(f, encoding='utf-8') as file:
        lines = file.readlines()
    return lines

txtfile = []
lines2 = []
for f in files:
    print(f"Handling: {f}")
    with open(f, encoding='utf-8') as file:
        lines = file.readlines()
    for line in lines:
        lines2.append(line)


with open('your_file.txt', 'w', encoding='utf-8') as f:
    for item in lines2:
        f.write("%s" % item)



