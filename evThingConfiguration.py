# coding=utf-8

from xml.etree.ElementTree import parse
from UtilGetPath import getRealPath

class ThingConfig:
    
    # class variables
    gw_id = ""
    gw_name = ""
    
    
    # object variable
    m_ThingList = []

    tree = None

    def __init__(self):
        # self.tree = parse("/home/pi/MPC-1/Configuration.xml")
        # self.tree = parse("/home/bananapi/campAgent/Configuration.xml")
        self.tree = parse(getRealPath() + "ThingConfiguration.xml")
        self._load()

    def _load(self):
        root = self.tree.getroot()
        self._parseController(root)
        self._parseThings(root)


    def _parseController(self, root):
        ctrlInfo = root.find("controller")
        ThingConfig.gw_id = ctrlInfo.find("id").text
        ThingConfig.gw_name = ctrlInfo.find("name").text

    def _parseThings(self, root):
        ThingInfo = root.find("things")

        for thing in ThingInfo.iter("thing"):
            thing_id = thing.text
            self.m_ThingList.append(thing_id)


    # -------------------------  exposed api -----------------------#

    def getThingList(self):
        return self.m_ThingList

















