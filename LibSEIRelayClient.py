# coding=utf-8

import threading
import socket
import time
from   UtilLog import plog, perr
import UtilTime
from  evThingConfiguration import ThingConfig
from threading import Lock

class SEIRelayClient(threading.Thread):


    def __init__(self, serverIP, serverPort, subIP, subPort, serverDataProcess):
        super(SEIRelayClient, self).__init__()

        self.m_socket = None

        self.m_szServerIP = serverIP
        self.m_nServerPort = serverPort
        self.m_serverDataProcess = serverDataProcess

        self.m_tKeepAliveTime = None
        self.m_bEnd = False

        self.m_connectionProblem = False

        self.m_sameTargetCounting = 0
        self.is_first_remote = True

        self.m_firstServerIP = serverIP
        self.m_firstServerPort = serverPort

        self.m_secondServerIP = subIP
        self.m_secondServerPort = subPort

        self.gateway_data_storage = None

        self.writer_lock = Lock()

    def setGatewayDataStorage(self,gateway_data_storage):
        self.gateway_data_storage = gateway_data_storage

    def hasConnectionProblem(self):
        return self.m_connectionProblem


    def terminateThread(self):
        self.m_bEnd = True

    def ip_change_process(self):
        self.m_sameTargetCounting = self.m_sameTargetCounting + 1

        if self.m_sameTargetCounting > 3 :  # 3번이상 안되면 ip 체인지
            self.m_sameTargetCounting = 0
            if self.is_first_remote == True :
                self.is_first_remote = False
                self.m_szServerIP = self.m_secondServerIP
                self.m_nServerPort = self.m_secondServerPort
            else :
                self.is_first_remote = True
                self.m_szServerIP = self.m_firstServerIP
                self.m_nServerPort = self.m_firstServerPort

    def connectToServer(self):
        plog("SVRCOMM.trying to reconnect to server", self.m_szServerIP, self.m_nServerPort)

        try:
            self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.m_socket.connect((self.m_szServerIP, self.m_nServerPort))
            self.m_tKeepAliveTime = UtilTime.getCurrentClock()
            plog("SVRCOMM.server connected..")
            self.m_connectionProblem = False
        except Exception, e:
            self.m_connectionProblem = True
            self.ip_change_process()
            plog("SVRCOMM.server connection fail.", str(e))
            return False

        return True


            
    def buffered_readlines(self):

        buffer = self.m_socket.recv(1024)
        if not buffer:
            yield ""

        buffering = True

        while buffering:
            if "\n" in buffer:
                (line, buffer) = buffer.split("\n", 1)
                yield line + "\n"
            else:
                more = self.m_socket.recv(1024)
                if not more:
                    buffering = False
                    yield ""
                else:
                    buffer += more
        if buffer :
            yield buffer        
            
    def run(self):
        plog("cmpServerComm.thread started...")
        while (not self.m_bEnd):

            if (not self.connectToServer()):
                plog("cmpServerComm.connectToServer error.")
                time.sleep(10)
                continue

            self.writeMessage(ThingConfig.gw_id)

            while (not self.m_bEnd and not self.m_connectionProblem):
                # self.checkKeepAlive()

                try:
                    # self.m_socket.settimeout(2)
                    for data in self.buffered_readlines():
                        if (data == None):
                            plog("cmpSEIRelayClient.data is none.")
                            self.closeSocket()
                            self.m_connectionProblem = True
                            break

                        if (data == ""):
                            plog("cmpSEIRelayClient.data is empty.")
                            self.closeSocket()
                            self.m_connectionProblem = True
                            break

                        plog("cmpSEIRelayClient.received data : {}".format(data))

                        self.executeData(data)

                except socket.timeout:
                    plog("SVRCOMM.recv time out.")
                    continue
                except socket.error:
                    self.closeSocket()
                    self.m_connectionProblem = True
                    plog("cmpMMARSClient socket error.")
                    break


        plog("cmpServerComm.thread terminated...")

    def executeData(self, szData):
        pass # kepco 버전에서는 데이터 수신 하는게 없다. 서버로 보고만 함. 
        #self.m_serverDataProcess.addJob(szData)

    def writeMessage(self, msg):

        with self.writer_lock:
            plog("cmpSEIRelayClient.writeMessage data : {}".format(msg))
            if msg is None :
                return False

            if self.m_connectionProblem is True:
                plog("[error] cmpMMARSClient.writeMessage to SEI-RELAY  fail.")
                if self.gateway_data_storage is not None:
                    self.gateway_data_storage.addMsg(msg)
                return False

            try:
                msg = msg + "\n"
                self.m_socket.send(msg)
            except Exception, e:
                plog("cmpMMARSClient.writeMessage to SEI-RELAY  fail.", str(e))
                self.closeSocket()
                self.m_connectionProblem = True
                return False

    def closeSocket(self):
        if self.m_socket:
            self.m_socket.close()
            self.m_socket = None




