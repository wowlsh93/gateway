# coding=utf-8
import socket
from UtilLog import plog

    
class UtilSockClient :
    m_szServerIP = "" 
    m_nPortNum = 0
    m_oSocket = None
    m_oParam = None
    
    def __init__(self, szServerIP, nPort) :
        self.m_szServerIP = szServerIP
        self.m_nPortNum = nPort
        self.m_oSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        

         
    def sendElectricToSAS(self, nodeId,  watt, pfcval , ipeak ) :
        szMessage = "{}\"node\" : {}, \"watt\" : {}, \"pfcval\" : {}, \"ipeak\" : {}{}".format("{", nodeId, watt, pfcval, ipeak, "}")
        self.m_oSocket.sendto(szMessage, (self.m_szServerIP, self.m_nPortNum))
        plog ("sendElectricToSAS send : " , szMessage)
        
        
        
    def sendElectricDetailToSAS(self, nodeId, listDetail):
        szListDetail = str(listDetail)
        szListDetail = szListDetail.replace("'", '"') # json 에서 ' 파싱을 못하고 있음.
        
        self.m_oSocket.sendto(szListDetail, (self.m_szServerIP, self.m_nPortNum))
        plog ("sendElectricDetailToSAS send : ", nodeId, self.m_szServerIP, self.m_nPortNum)
        
    
        
    
    def sendSockPacket(self, nCmd, nType, nVal) :
        szMessage = "{}\"cmd\" : {}, \"type\" : {}, \"val\" : {}{}".format("{", nCmd, nType, nVal, "}")
        self.m_oSocket.sendto(szMessage, (self.m_szServerIP, self.m_nPortNum))
        plog ("DATA Sent.", self.m_szServerIP, self.m_nPortNum)
    
    """
        1 : on
        2 : off
        3 : flash
        4 : fade
        5 : red
        6 : green
        7 : blue
        8 : white
    """
         
    def reqLedState(self, nVal) :
        self.sendSockPacket(1, 3, nVal)



    
                
                