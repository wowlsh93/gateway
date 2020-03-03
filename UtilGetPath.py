# coding=utf-8
import os

def getRealPath() :
    szRealPath = os.path.realpath(__file__)

    nIdx = szRealPath.find("UtilGetPath.py") # 자신의 파일명 또는 pyc 일 수 있다.
    
    return szRealPath[:nIdx]

