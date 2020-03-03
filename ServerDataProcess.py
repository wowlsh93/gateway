# coding=utf-8

import simplejson
from UtilLog import plog, logException
from UtilLog import perr
from evPKConst import PKConst
from evLock import evAutoThreadLock

import time
import threading


class JsonJob:
    def makeJsonObject(self, szData):
        return simplejson.loads(szData)

    def setJsonData(self, szData):
        self.m_oJson = self.makeJsonObject(szData)

    def getJsonData(self):
        return self.m_oJson

    def printJob(self):
        plog(self.m_oJson)


class ServerDataProcess(threading.Thread):


    m_aJobList = []  # 양방향에서 온 잡 리스트
    m_bEnd = False
    
    def __init__(self,oThingManager, oGate):
        super(ServerDataProcess, self).__init__()
        self.m_oLock = threading.Lock()
        self.oThingManager= oThingManager
        self.oGate = oGate
      

    def terminateThread(self):
        self.m_bEnd = True
        

    def addJob(self, szData):

        # syncronized
        evAutoThreadLock(self.m_oLock)
        plog("JobManager:addJob : ", szData)

        oJob = JsonJob()

        try:
            oJob.setJsonData(szData)
            self.m_aJobList.append(oJob)
        except:
            perr("JobManager.addJob  exception!!.", szData)

        #del oLock


    def getJob(self):

        if (len(self.m_aJobList) == 0):
            return None

        evAutoThreadLock(self.m_oLock)

        job = self.m_aJobList.pop(0)  # PIPO

        #del oLock

        return job

    # main thread 에 의해 수행
    def run(self):

        while (not self.m_bEnd):
            oJob = self.getJob()
            if (oJob == None):
                time.sleep(0.1)
                continue

            oJob.printJob()

            oJson = oJob.getJsonData()
            
            try:
                self.processFromSEIRelay(oJson)
            except Exception, e:
                #perr("cmpJobManager.procJob.processFromSEIRelay error", str(e))
                logException()
                
    

    def processFromSEIRelay(self, recvJson):

        if (PKConst.cmd in recvJson):
            cmd = recvJson[PKConst.cmd]

            if (cmd ==  PKConst.ip_change):
                EvConfig.set("datastorage", "servername" , recvJson[PKConst.content])
            else:
                self.oThingManager.processData(recvJson, self.oGate)

   



