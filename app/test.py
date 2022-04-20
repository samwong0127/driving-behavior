import time
import threading
import os

def func1():
    os.system("python application.py")

def func2():
    os.system("python write.py")

threads = []
t1 = threading.Thread(target = func1)
threads.append(t1)
t2 = threading.Thread(target = func2)
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    
    t.join()
