import csv
import re
import clr
import sys
import System
import time
from System.Collections import *

sys.path.append("c:\\Program Files (x86)\\National Instruments\\VeriStand 2020\\nivs.lib\\Reference Assemblies")
clr.AddReference("NationalInstruments.VeriStand.SystemDefinitionAPI")
clr.AddReference("NationalInstruments.VeriStand.ClientAPI")
clr.AddReference("NationalInstruments.VeriStand")

from NationalInstruments.VeriStand.SystemDefinitionAPI import SystemDefinition, NodeIDUtil, Dictionary
from NationalInstruments.VeriStand.ClientAPI import Factory, SystemState
from NationalInstruments.VeriStand import Error


class CarMakerChannels:
    nodeIDUtil = NodeIDUtil()
    def __init__(self, systemDefinitionObject):
        self.systemDefinitionObject = systemDefinitionObject
        self.GetCarMakerNodeID()
        self.GetCarMakerInputChannelID()
        self.NrOfExistingChannels()
        self.GetCarMakerInputChannelGUID()
        self.AddChannelToCarMaker()
        self.SaveSystemDefFile()

    # Get NodeID for the current setup CustomDevices
    def GetCarMakerNodeID(self):
        # List targets custom devices and their ID
        firstTarget = self.systemDefinitionObject.Root.GetTargets().GetTargetList()[0]
        customDevices_objects = firstTarget.GetCustomDevices().GetCustomDeviceList()
        [print("CustomDeviceName: ", i.Name, "NodeID: ", i.NodeID,"BaseNodeType: ", i.BaseNodeType) for i in customDevices_objects]
        #[print("CarMaker ID: ",i.NodeID) for i in customDevices_objects if i.Name == "CarMaker"]

        # Find NodeID for CarMaker Custom Device
        carMakerData = [i.NodeID for i in customDevices_objects if i.Name == "CarMaker"]
        carMakerID = carMakerData[0]
        self.carMakerID = carMakerID

    # Get ID of Input section 
    def GetCarMakerInputChannelID(self):
        customDeviceToEdit = self.nodeIDUtil.IDToCustomDevice(self.carMakerID)
        [print("SectionName: ", i.Name, "NodeID: ", i.NodeID, "BaseNodeType: ", i.BaseNodeType) for i in customDeviceToEdit.GetChildren()]
        carMakerChannelID = [i.NodeID for i in customDeviceToEdit.GetChildren() if i.Name == "Inputs"]
        self.carMakerInputChannelID = carMakerChannelID[0]

    # def NrOfExistingChannels():
    def NrOfExistingChannels(self):
        channelList  = self.nodeIDUtil.IDToCustomDeviceSection(self.carMakerInputChannelID).GetChildren()
        self.nrOfChannels = len(channelList)

    # # Get NodeID's of CD channels
    def GetCarMakerInputChannelGUID(self):
        nodeIDUtil = NodeIDUtil()
        channelList  = nodeIDUtil.IDToCustomDeviceSection(self.carMakerInputChannelID).GetChildren()
        #[print("Name3",i.Name,"ID3",i.NodeID,"GUID", i.TypeGUID) for i in channelList]
        carMakerChannelGUID = [i.TypeGUID for i in channelList]
        self.carMakerInputChannelGUID = carMakerChannelGUID[0]

    def AddChannelToCarMaker(self):
        # Add Channel to section. Alla kanaler i Iput sektionen har samma GUID
        newItem = System.Boolean(False)
        index = self.nrOfChannels+1
        indexedChannelName = "myChannel_"+"{}".format(index)
        CD_channel, newItem_out  = self.nodeIDUtil.IDToCustomDeviceSection(self.carMakerInputChannelID).AddCustomDeviceChannelIfNotFound(indexedChannelName,self.carMakerInputChannelGUID,newItem)
        print("Channel with name:", CD_channel.Name, " added")

    def SaveSystemDefFile(self):
        error = System.String("")
        error_out = System.String("")
        status, error_out = systemDefinitionObject.SaveSystemDefinitionFile(error)
        print("SystemDefinitionFile Saved with status: ",status,error_out)

if __name__ == '__main__':
    systemDefinitionFilePath = r"C:\Users\dsamuels\Documents\VeriStand Projects\Engine Demo 26\Engine Demo.nivssdf"
    systemDefinitionObject = SystemDefinition(systemDefinitionFilePath)

    carMakerChannels = CarMakerChannels(systemDefinitionObject)
    #print(dir(carMakerChannels))