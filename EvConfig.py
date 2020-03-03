# coding=utf-8
import os
import LibXml

class EvConfig :
    def __init__(self) :
        # path 를 저장하는 xml 경로는 실제 경로로 찾을 수밖에 없음
        szRealPath = os.path.realpath(__file__)
        szPaths = szRealPath[:szRealPath.find("EvConfig")] + "EvGate.xml"
        
        #self.m_szXmlPath = "EvGate.xml"
        self.m_szXmlPath = szPaths
        self.m_oXmlRoot = None
        self.m_szDefaultGwGey = "v*@7sjsl*(1.,;x0" # xml 저장할 때 사용되는 기본 암호화 키
        
        self._readRoot()
    
    def _readRoot(self) :
        self.m_oXmlRoot = LibXml.readXmlRoot(self.m_szXmlPath)

    def get(self, szSection, szField, defaultVal = None) :
        oElement = LibXml.getXmlElement(self.m_oXmlRoot, szSection)
        if (oElement == None) :
            return defaultVal
        val = LibXml.getXmlValue(oElement, szField)
        if (val == None) :
            return defaultVal
        
        return val
    
    def set(self, szSection, szField, szValue) : 
        oElement = LibXml.getXmlElement(self.m_oXmlRoot, szSection)
        LibXml.setXmlValue(oElement, szField, szValue)
        LibXml.writeXmlRoot(self.m_szXmlPath, self.m_oXmlRoot)

    # def getSk1(self) :
    #     szZey = self.get("cipher", "key")
    #     if (szZey == None) :
    #         return ""
    #
    #     obj = AESCipher(self.m_szDefaultGwGey)
    #
    #     return obj.decrypt(szZey)

"""
oTest = EvConfig()

print oTest.get("terminal", "name")
print oTest.get("terminal", "port")
print oTest.get("terminal", "id")
print oTest.get("terminal", "passwd")


print oTest.getSk1()
"""
