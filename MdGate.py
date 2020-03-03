# coding=utf-8

import threading

from MdGateInterface import MdGateServerApi
from MdGateServer import MdGateServer

from UtilLog import plog, logException

class MdGate (MdGateServerApi) :
    def __init__(self, oGateMain) :

        self.m_bGateFlag = False
        self.m_oGateMain = oGateMain

        MdGateServerApi.__init__(self)
        
        self.m_oGateServer = MdGateServer(oGateMain, self)
        
    def startGateThread(self) :
        self.m_bGateFlag = True
        threading.Timer(0, MdGate.procGateServerThread, (self,)).start()

    def terminGateThread(self) :
        self.m_bGateFlag = False

    @staticmethod
    def procGateServerThread(oMdGate) :
        plog ("MdGateSvrThread start..")
        oMdGate.procGateServer()
        plog ("MdGateSvrThread terminated..")

            
    def procGateServer(self) :
        while (self.m_bGateFlag) :
            try :
                self.m_oGateServer._procGateServer(self.m_oJobManagerSvr)
            except :
                logException()
        




















































