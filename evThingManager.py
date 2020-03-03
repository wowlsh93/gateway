# coding=utf-8
'''
Created on 2015. 2. 9.

@author: brad
'''

from UtilLog import perr
from UtilLog import plog


class ThingManager:
    def __init__(self, config):
        self.m_aThingList = None
        self.m_oConfig = config
        self.reload(self.m_oConfig)
 

    def reload(self, oConfig):
        self.m_aThingList = oConfig.getThingList()

    def processData(self, recvJson , oGate):
        pass
#     
#             # call id
#             #callId = recvJson[PKConst.call_id]
#     
#             # thing id
#             switchId = recvJson[PKConst.switch_id]
#     
#             # command
#             cmd = recvJson[PKConst.cmd]
#     
#             # content
#             if PKConst.content in recvJson:
#                 content = recvJson[PKConst.content]
#     
#             if switchId == None:
#                 return
#     
#             # 콘센트 켜줘~
#             if cmd == PKConst.switch_on:
#                 pass
#             # 나중에 content 를 파싱해서 nMaxWatt, nMaxWattSec 2개의 값을 파라미터로 전달하라.
#             elif cmd == PKConst.pattern_option_change:
#                 pat = content.split(":")
#                 for id in self.m_aThingList:
#                     oGate.setEvParam(int(id) , int(pat[0]) , int(pat[1]))
#     
#             elif cmd == PKConst.card_auth:
#                 oGate.rfidAuthResponse(int(switchId) , 1 if content == PKConst.auth_success else 0)
#     
#             elif cmd == PKConst.meter_electricity_get:
#                 oGate.EvMeterRequest(int(switchId))
#             else:
#                 plog("No defined cmd received !!")

  

