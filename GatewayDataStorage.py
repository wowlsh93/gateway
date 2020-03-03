# coding=utf-8
# 서버로의 네트워크가 단절시, 데이터를 모아두는 버퍼역할을 한다. 서버 재접속되면 여기 모인 데이터를 보내준다.
import simplejson
from UtilLog import plog, logException
from UtilLog import perr
import time
import threading
import Queue


class GatewayDataStorage(threading.Thread):
    m_aDataList = Queue.Queue(300000)
    m_bEnd = False

    def __init__(self, oSeiRelay):
        super(GatewayDataStorage, self).__init__()
        self.oSeiRelay = oSeiRelay
        self.oSeiRelay.setGatewayDataStorage(self)


    def terminateThread(self):
        self.m_bEnd = True

    def addMsg(self, szData):

        try:
            self.m_aDataList.put(szData)
            print(self.m_aDataList.qsize())
        except:
            perr("GatewayDataStorage.addJob  exception!!.", szData)


    def getMsg(self):

        if (self.m_aDataList.empty()):
            return None

        msg = self.m_aDataList.get()

        return msg

    # main thread 에 의해 수행
    def run(self):

        while (not self.m_bEnd):
            if self.oSeiRelay.hasConnectionProblem() == False:
                msg = self.getMsg()
                if (msg == None):
                    time.sleep(1)
                    continue


                try:
                    self.oSeiRelay.writeMessage(msg)
                    time.sleep(0.5)
                except Exception, e:
                    perr("GatewayDataStorage  error", str(e))
                    logException()
            else: # oSeiRelay에 문제가 있으면 10초 기다리자.
                time.sleep(1)



