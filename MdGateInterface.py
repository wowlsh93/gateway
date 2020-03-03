# coding=utf-8
import LibEvent
from Job import Job

from JobManager import JobManager

from UtilLog import plog, perr, logException

class MdGateBaseApi :
    def _procJob(self, jobId, jobData, jobManager, jobEvent, bSync) :
        # Job(JOB_ID, [data], sync-event)
        oJob = Job(jobId, jobData, jobEvent)
        jobManager.addJob(oJob) # add to list




# 서버에서 제공하는 api
class MdGateServerApi (MdGateBaseApi) :
    def __init__(self) :
        self.m_oEventSvr = LibEvent.LibEvent() # object for sync
        self.m_oJobManagerSvr = JobManager()

    ###########################################################################
    # 기본 내부 멤버
    def procJobSvr(self, jobId, jobData, bSync = 0) :
        return self._procJob(jobId, jobData, self.m_oJobManagerSvr, self.m_oEventSvr, bSync)
    
    ###########################################################################
    """
    # 추가하는 api
    # 1. Job_EV_SERVER_SYNC_SAMPLE 과 같은 Job 종류 정의
    # 2. 아래의 api 펑션의 파라미터 정의
    # 3. MdGateServer 에서 해당 job 처리
    """ 
    def procSyncServerExample(self, nSample) :
        # Job_EV_SERVER_SYNC_SAMPLE : JobZWElectric.py 참조
        oJob = self.procJobSvr(Job.Job_EV_SERVER_SYNC_SAMPLE, (nSample, 1, "test string", 3), 0)
        return oJob
    
    def setPowerStreamInfo(self, nNodeId, nClock, nCount, arWatt, arPf) :
        oJob = self.procJobSvr(Job.Job_ZW_ELEC_STREAM_TO_SERVER, (nNodeId, nClock, nCount, arWatt, arPf), 0)
        return oJob

    def repVrmsInfoPerMin(self, nNodeId, nClock, nVrmsAvg, nVrmsMax, nVrmsMin) :
        oJob = self.procJobSvr(Job.Job_ZW_ELEC_STREAM_REP_VRMS_INFO, (nNodeId, nClock, nVrmsAvg, nVrmsMax, nVrmsMin), 0)
        return oJob








