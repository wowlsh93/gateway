# coding=utf-8

#=============================================================
"""
g_szLogName = "evgate"
g_szApplPath = "/Project/Work/Ev-Charger/EvGate/"
g_szLogRootPath = g_szApplPath + "log/"
g_szLogPath = g_szLogRootPath + g_szLogName + "_{}{}.log"
g_szTarName = g_szLogName + "_{}.tar"
g_szTarPath = g_szLogRootPath + g_szTarName
g_szGzPath  = g_szLogRootPath + g_szLogName + "_{}.gz"

"""
import platform

# my pc 로그 패스, xml 에서 변경할 것

g_szApplPath = "/home/pi/gateway-testunit/"

if platform.system() == "Windows":
    g_szApplPath = "D:\work\git\SAS\gateway-testunit"


#g_szApplPath = "D:/"

# 기타 설정
# 다른 py에서 from evcomm import g_szlogname 같은 경우 미리 복사가 된다. 이쪽을 나중에 바꾸어도 다른 py는 안바뀜
g_szLogName = "evgate"

g_szLogRootPath = ""
if platform.system() != "Windows":
    g_szLogRootPath = g_szApplPath + "log"
g_szLogRootPath = "D:\work\git\SAS\gateway-testunit\log"
g_szLogPath = g_szLogRootPath + g_szLogName + "_{}{}.log"
g_szTarName = g_szLogName + "_{}.tar"
g_szTarPath = g_szLogRootPath + g_szTarName
g_szGzPath  = g_szLogRootPath + g_szLogName + "_{}.gz"

#"""
def setPathSerial(szApplPath) :
    global g_szLogName, g_szApplPath, g_szLogRootPath, g_szLogPath, g_szTarName, g_szTarPath, g_szGzPath
    
    print ("--- setPathSerila. app path : ", szApplPath)
    
    g_szLogName = "evgate"
    g_szApplPath = szApplPath
    g_szLogRootPath = g_szApplPath + "log/"
    g_szLogPath = g_szLogRootPath + g_szLogName + "_{}{}.log"
    g_szTarName = g_szLogName + "_{}.tar"
    g_szTarPath = g_szLogRootPath + g_szTarName
    g_szGzPath  = g_szLogRootPath + g_szLogName + "_{}.gz"
    
def getAppPath() :
    global g_szApplPath
    return g_szApplPath

def getLogPath() :
    global g_szApplPath, g_szLogName, g_szLogRootPath, g_szLogPath, g_szTarName, g_szTarPath, g_szGzPath
    return [g_szApplPath, g_szLogName, g_szLogRootPath, g_szLogPath, g_szTarName, g_szTarPath, g_szGzPath]



#=============================================================
g_bLinux = False                # linux or windows
g_bLogToConsole = True            # log 를 console로 출력할지
g_bLogPacket = True             # packet 로그 활성화
g_bServerEnable = False
#g_szApplVersion = "1.0.0" ev charger
g_szApplVersion = "2.0.1"
