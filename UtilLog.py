# coding=utf-8
import os, sys, traceback
import shutil
import time
import tarfile
import threading
from UtilTime import getCurrentStrSecTime, getCurrentStrDate, getCurrentClock, getDateTimeFromIndex
from EvCommon import getLogPath 
""" 
0 : g_szApplPath, 
1 : g_szLogName, 
2 : g_szLogRootPath, 
3 : g_szLogPath, 
4 : g_szTarName, 
5 : g_szTarPath, 
6 : g_szGzPath
""" 



#=============================================================



g_bLogConsole = 0

def setLogToConsole(nEnable) :
    global g_bLogConsole
    g_bLogConsole = nEnable

# log 파일명에 추가 첨자
def getLogFileName(szAdd = "") :
    return getLogPath()[3].format(getCurrentStrDate(), szAdd)


#=============================================================
# try 오류날 때 error log 출력   
#=============================================================
traceback_template = '''Traceback (most recent call last):
    File "%(filename)s", line %(lineno)s, in %(name)s
    %(type)s: %(message)s\n''' # Skipping the "actual line" item

def logException() :
    exc_type, exc_value, exc_traceback = sys.exc_info()
    
    traceback_details = {
                         'filename': exc_traceback.tb_frame.f_code.co_filename,
                         'lineno'  : exc_traceback.tb_lineno,
                         'name'    : exc_traceback.tb_frame.f_code.co_name,
                         'type'    : exc_type.__name__,
                         'message' : exc_value.message, # or see traceback._some_str()
                        }
    
    del(exc_type, exc_value, exc_traceback) # So we don't leave our local labels/objects dangling
    # This still isn't "completely safe", though!
    # "Best (recommended) practice: replace all exc_type, exc_value, exc_traceback
    # with sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]
    
    perr(traceback_template % traceback_details)
    perr(traceback.format_exc())
    

"""
setLogToConsole(1)
try :
    file.open("test.txt")
except :
    logException()
"""

#=============================================================
# control 모드일 때 로그를 직접 보기 위해 콘솔로 출력하는 부분을 추가
def writeFile(szAdd, szMsg) :
    global g_bLogConsole
    if (g_bLogConsole == 1) :
        print szMsg
        return
    
    with open(getLogFileName(szAdd), "a") as dFile :
        dFile.write(szMsg + "\n")
        dFile.close()

# console 에 명시적 출력 - daemon 일 경우 죽을 수 있다.
def plogc(*arg, **keywords) :
    szData = ""
    
    for szItem in arg :
        szData += str(szItem) + " "

    szPrint = getCurrentStrSecTime() + " " + szData
    
    try :
        print(szPrint)
    except Exception, e :
        plog ("plogc error : ", str(e))

# 일반 로그 출력 함수
def plog(*arg, **keywords) :
    szData = ""
    
    for szItem in arg :
        szData += str(szItem) + " "

    szPrint = getCurrentStrSecTime() + " " + szData
    print(szPrint)
    writeFile("", szPrint)

# 임시로 따로 저장하는 로그(tmp) 출력 함수, 확인 후 plog 로 변경할 것
def plog2(*arg, **keywords) :
    szData = ""
    
    for szItem in arg :
        szData += str(szItem) + " "

    szPrint = getCurrentStrSecTime() + " " + szData
    print(szPrint)
    writeFile("_tmp", szPrint)

# error 로그 출력 함수, _error 에 저장
def perr(*arg, **keywords) :
    szData = ""
    
    for szItem in arg :
        szData += str(szItem) + " "

    szPrint = getCurrentStrSecTime() + " " + szData
    print(szPrint)
    #writeFile("", szPrint)
    writeFile("_error", szPrint)


#=============================================================
# 로그 압축 수행
# 날짜 변경 시 tar 로 모은 후 달 변경 시 압축한다.
# 한달동안 모인 tar 크기가 상당하다. 압축 후에 tar 로 모으는 것을 테스트

# 날짜 변경 체크
# 이전 날짜가 없는 경우 pass
# 이전 날짜 로그를 압축 후 tar 에 add



g_bCompThread = False

# appl 시작시 콜, 5초 후 thread 가동
def startCheckLogFileThread() :
    global g_bCompThread
    
    g_bCompThread = True
    threading.Timer(0, checkLogFile, ).start()

# appl 종료시 콜, thread flag 설정으로 close
def terminCheckLogFileThread() :
    global g_bCompThread
    
    g_bCompThread = False


""" 
0 : g_szApplPath, 
1 : g_szLogName, 
2 : g_szLogRootPath, 
3 : g_szLogPath, 
4 : g_szTarName, 
5 : g_szTarPath, 
6 : g_szGzPath
""" 
from EvCommon import getLogPath 


g_szLogDate = ""
def checkLogFile() :
    global g_szLogDate
    
    logPathConfig = getLogPath()
    
    plog ("log compression thread start..")
    
    while (g_bCompThread) :
        time.sleep(5)
        
        szCurDate = getCurrentStrDate()
        if (g_szLogDate == "") :
            g_szLogDate = szCurDate
        
        # 날짜가 달라짐
        if (szCurDate != g_szLogDate) :
            
            # 다른 thread가 로그 기록중일 수 있으므로, 초단위 체크
            nSec = getDateTimeFromIndex(getCurrentClock(), 5)
            if (nSec == 0) :
                continue

            plog ("log compression start..", g_szLogDate)

            szGzPath = logPathConfig[6].format(g_szLogDate)
            szTarPath = logPathConfig[5].format(g_szLogDate[0:7])

            # 로그파일을 압축 후 tar 로 모은다.
            tar = None
            try :
                # 압축된 파일이 없어도 생성됨.
                tar = tarfile.open(szGzPath, "w:gz")
                
                for szAdd in ("", "_tmp", "_error") :
                    szLogPath = logPathConfig[3].format(g_szLogDate, szAdd)
                    
                    if (os.path.isfile(szLogPath)) :
                        # 먼저 압축, 뒤는 압축할 파일명, 없으면 전체경로를 저장한다.
                        tar.add(szLogPath, "{}_{}{}.log".format(logPathConfig[1], g_szLogDate, szAdd))
                        os.remove(szLogPath)
                        plog ("log added to gz", szLogPath)
                    else :
                        plog ("log not found.", szLogPath)
                        
                tar.close()
                
            except Exception, e :
                logException()
                if (tar != None) :
                    tar.close()
                


            # 후에 tar 로 취합, 원래는 tar --> gz 인데 gz 에서 append 를 못찾음
            if (os.path.isfile(szGzPath)) :
                tar = tarfile.open(szTarPath, "a")
                tar.add(szGzPath, "{}_{}.gz".format(logPathConfig[1], g_szLogDate))
                tar.close()
                os.remove(szGzPath)
                plog ("gz added to tar", szGzPath)
            else :
                plog ("gz not found", szGzPath)

            plog ("log compression end..", szTarPath)

            # 월이 달라지면, 월폴더로 이동
            if (szCurDate[5:7] != g_szLogDate[5:7]) :
                tarBackup = logPathConfig[2] + g_szLogDate[0:4]
                tarBackupFile = "{}{}/{}".format(logPathConfig[2], g_szLogDate[0:4], logPathConfig[4].format(g_szLogDate[0:7])) 
                plog ("tarBackup : ", tarBackup, tarBackupFile)
                
                if (not os.path.isdir(tarBackup)) :
                    os.mkdir(tarBackup)

                shutil.move(szTarPath, tarBackup)

            g_szLogDate = szCurDate



        
    plog ("log compression thread terminated..")
    

#=============================================================
# 로그 compression test func
"""
def logCompTestFunc() :
    global g_szLogDate
    
    setLogToConsole(0)
    
    plog ("start")
            
    startCheckLogFile()
    g_szLogDate = "2016-10-03"
    
    time.sleep(7)
    terminCheckLogFile()
    
    plog ("end")

logCompTestFunc()
"""





