# coding=utf-8
import EvGateRun
EvGateRun.gateMain()


"""
import threading
import UtilTime


def makethread() :
    cLock = threading.Lock()
    for idx in range(10) :
        threading.Timer(0, calc, (idx, cLock)).start()

def calc(nIdx, cLock) :
    
    idxres = 0
    idx2res = 0
    idx3res = 0
    
    tTime = UtilTime.getCurrentClock()
    
    for idx1 in range(10000) :
        for idx2 in range(1000) :
            idxres = idx1 + idx2
        
    tTime2 = UtilTime.getCurrentClock()
    
    cLock.acquire()
    print "idx : ", nIdx, ", time : ", tTime2 - tTime
    cLock.release()


makethread()
"""
