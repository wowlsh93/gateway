# coding=utf-8

from Job import Job
from UtilLog import plog, perr, logException
from  evThingConfiguration import ThingConfig
from evPKConst import PKConst
import simplejson
import time
import UtilTime
from DBManager import InfluxDBManager

"""
api 추가할 때
id - JobEvService
api - MdGateInterface
구현 - 여기
"""
class MdGateServer :
    def __init__(self, oGateMain, oMdGate) :
        self.m_oGateMain = oGateMain
        self.m_oGateInterface = oMdGate
        # device api 콜할 때 self.m_oGateInterface.setEvParam(...)
      
    
    def setSeiRelayClient(self,oSeiRelay):
        self.oSeiRelay = oSeiRelay
        
    ######################################################
    def _procGateServer(self, oJobManager) :
        # nUgjCnt, njCnt = oJobManager.waitForJob(1)
        # if (nUgjCnt == 0 and njCnt == 0) :
        #     return
        #
        # oJob = None
        #
        # if (nUgjCnt > 0) :
        #     oJob = oJobManager.getUgJob()
        # elif (njCnt > 0) :
        #     oJob = oJobManager.getJob()
        # if (oJob == None) :
        #     perr ("MdGateD. job is none. logic error.")
        #     return
        #
        # ########################################################
        # """
        # # 정의한 job 이 호출되었을 때 여기에서 처리 후
        # # job 에 결과를 저장 후 job event 알림
        # """
        # if (oJob.m_nCmd == Job.Job_EV_SERVER_SYNC_SAMPLE) :
        #     # 실제로 데이터를 처리하는 함수
        #     self.procServerSyncSample(oJob)
        #
        # elif (oJob.m_nCmd == Job.Job_ZW_ELEC_STREAM_TO_SERVER) :
        #     self.procWattToServer(oJob)
        # elif (oJob.m_nCmd == Job.Job_ZW_ELEC_STREAM_REP_VRMS_INFO) :
        #     self.procPowerToServer(oJob)
        # else :
        #     perr("_procGateServer.undefined Job.", oJob.m_nCmd)
        #     oJob.resError()

        while True:
            self.procWattToServer_test()



    def procWattToServer_test(self):

        self.from_influxdb()



    def from_influxdb(self):

        from_oInfluxDB = InfluxDBManager("192.168.1.192", 8086, "root", "root", "power", "inf")  # 오리지널 DB 명

        watts = []
        pfs = []

        chunck_size = 20  # 20 * 1초  (1초)
        i = 0
        for watt, pf, data_time in from_oInfluxDB.getWatt_by_range("rpi058", 2,  '50ms', '2018-01-14 09:36:00',
                                                              '2018-01-14 11:00:00', None):

            if i != chunck_size:
                watts.append(float(watt))
                pfs.append(pf)

                i += 1
            else:

                json_packet = self.makeWattMessage(2, UtilTime.getCurrentClock(), 20, watts, pfs)
                self.oSeiRelay.writeMessage(json_packet)

                json_packet = self.makeWattMessage(3, UtilTime.getCurrentClock(), 20, [ w *  0.9 for w  in watts] , pfs)
                self.oSeiRelay.writeMessage(json_packet)

                json_packet = self.makeWattMessage(4, UtilTime.getCurrentClock(), 20, [ w *  1.1 for w  in watts] , pfs)
                self.oSeiRelay.writeMessage(json_packet)


                i = 0
                watts = []
                pfs = []
                time.sleep(1)





        print ("########### data insert finished!! ################")


    ######################################################
    def procServerSyncSample(self, oJob) :
        plog ("processing server svr sample job..")
        
        plog ("job data : ", oJob.m_val)
        
        if (1) :
            # 처리 결과 저장
            oJob.resServerSync(2) # 동기식일 때 결과를 알린다. 비동기여도 결과를 체크하는 경우 결과를 알리는데 사용할 수 있다.
            return
        elif (0) :
            # 처리 결과 저장
            oJob.resError() # 동기식일 때 결과를 알린다. 비동기여도 결과를 체크하는 경우 결과를 알리는데 사용할 수 있다.
            return
        else :
            oJob.resOk()
            return


    #(nNodeId, nClock, nVrmsAvg, nVrmsMax, nVrmsMin)
    def procPowerToServer(self, oJob) :
        plog ("procPowerToServer called.", oJob.m_val)
        json_packet = self.makePowerMessage(oJob.m_val[0], oJob.m_val[1], oJob.m_val[2], oJob.m_val[3], oJob.m_val[4])   
        self.oSeiRelay.writeMessage(json_packet)
        
        oJob.resOk()     

   
    def makeWattMessage(self, id, nclock, ncount, arwatt, arpf):

        packet = simplejson.JSONEncoder().encode(
            {
             PKConst.gateway_id : ThingConfig.gw_id,
             PKConst.switch_id  : id,
             PKConst.cmd        : PKConst.cmd_watt,
             PKConst.time       : nclock,
             PKConst.count      : ncount,
             PKConst.watts      : arwatt,
             PKConst.pfs        : arpf
             }
        )

        return packet
  

    def makePowerMessage(self, id, nclock, nVrmsAvg, nVrmsMax, nVrmsMin):

        packet = simplejson.JSONEncoder().encode(
            {
             PKConst.gateway_id : ThingConfig.gw_id,
             PKConst.switch_id  : id,
             PKConst.cmd        : PKConst.cmd_power,
             PKConst.time       : nclock,
             PKConst.vrms_avg   : nVrmsAvg,
             PKConst.vrms_max   : nVrmsMax,
             PKConst.vrms_min   : nVrmsMin
             }
        )

        return packet
  

    
    
