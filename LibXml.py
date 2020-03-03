# coding=utf-8
from UtilLog import plog, perr, logException
from xml.etree.ElementTree import Element, ElementTree, SubElement, dump, parse, tostring

def readXmlRoot(szFilePath) :
    try :
        oFile = open(szFilePath, "r")
        if (oFile == None) :
            return None

        oTree = parse(oFile)
        oFile.close()
        
        return oTree.getroot()
    
    except :
        logException()
        
    return None
    
    
def writeXmlRoot(szFilePath, oXmlRoot) :
    try :
        ElementTree(oXmlRoot).write(szFilePath)
    except :
        logException()
    
    return


def getXmlElements(oXmlElement, szEleName) :
    try :
        return oXmlElement.findall(szEleName)
    except :
        logException()
    
    return None

def getXmlElement(oXmlElement, szEleName) :
    try :
        oElements = oXmlElement.findall(szEleName)
        if (oElements == None) :
            return None
        if len(oElements) == 0 :
            return None
        return oElements[0]
    except :
        logException()
    
    return None

#=============================================================
def createXmlElement(szName) :
    try :
        return Element(szName)
    except :
        logException()
    
    return None

def addXmlElement(oXmlElement, oElement) :
    try :
        oXmlElement.append(oElement)
    except :
        logException()
        

#=============================================================
def removeXmlElement(oXmlElement, oElement) :
    try :
        oXmlElement.remove(oElement)
    except :
        logException()
    
#=============================================================
def getXmlValue(oXmlElement, szValName) :
    try :
        return oXmlElement.findtext(szValName)
    except :
        logException()
    
    return None

def setXmlValue(oElement, szName, szValue) :
    try :
        oSubElement = oElement.find(szName)
        if (oSubElement == None) :
            SubElement(oElement, szName).text = szValue
        else :
            oSubElement.text = szValue
    except :
        logException()

"""
def setXmlValue(oXmlElement, szValName, szValue) :
    try :
        oXmlElement.find(szValName).text = szValue
    except :
        logException()
    
    return
"""

#=============================================================
# xml 을 보기좋게 정렬하는 함수
def indent(elem, level=0) :
    try :
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
    except :
        logException()



"""
import UtilLog
UtilLog.setLogToConsole(1)

oRoot = readXmlRoot("EvGate.xml")

oElement = getXmlElement(oRoot, "telnet")

oVal = getXmlValue(oElement, "port")

print "telnet port : ", oVal


setXmlValue(oElement, "port", "14332")

oVal = getXmlValue(oElement, "port")

print "telnet port : ", oVal

writeXmlRoot("EvGate.xml", oRoot)
"""



















