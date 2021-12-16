import csv
import re
import clr
import sys
import System
import time
from System.Collections import *
from System.Collections.Generic import Dictionary as Dictionaryy
sys.path.append("c:\\Program Files (x86)\\National Instruments\\VeriStand 2020\\nivs.lib\\Reference Assemblies")
clr.AddReference("NationalInstruments.VeriStand.SystemDefinitionAPI")
clr.AddReference("NationalInstruments.VeriStand.ClientAPI")
clr.AddReference("NationalInstruments.VeriStand")

from NationalInstruments.VeriStand.SystemDefinitionAPI import SystemDefinition, NodeIDUtil, Dictionary
from NationalInstruments.VeriStand.ClientAPI import Factory, SystemState
from NationalInstruments.VeriStand import Error

# Open reference to SystemDefinition

systemDefinitionFilePath = r"C:\Users\dsamuels\Documents\VeriStand Projects\Engine Demo 26\Engine Demo.nivssdf"
systemDefinitionObject = SystemDefinition(systemDefinitionFilePath)


# GetChannelMappings, Read current mapped signals

# pythonPlaceHolder,channelPathSources_returned,channelPathDestinations_returned  = systemDefinitionObject.Root.GetChannelMappings(channelPathSources,channelPathDestinations)

# Get NodeID for the current setup CustomDevices
firstTarget = systemDefinitionObject.Root.GetTargets().GetTargetList()[0]
customDevices_objects = firstTarget.GetCustomDevices().GetCustomDeviceList()
[print("Name: ", i.Name, "NodeID: ", i.NodeID,"BaseNodeType: ", i.BaseNodeType) for i in customDevices_objects]

[print("CarMaker ID: ",i.NodeID) for i in customDevices_objects if i.Name == "CarMaker"]
carMakerData = [i.NodeID for i in customDevices_objects if i.Name == "CarMaker"]
carMakerID = carMakerData[0]

# Setup CustomDevice to edit, using NodeID that is read from systemdefinition
nodeIDUtil = NodeIDUtil()
customDeviceToEdit = nodeIDUtil.IDToCustomDevice(carMakerID)
[print("Name: ", i.Name, "NodeID: ", i.NodeID, "BaseNodeType: ", i.BaseNodeType) for i in customDeviceToEdit.GetChildren()]
carMakerChannelID = [i.NodeID for i in customDeviceToEdit.GetChildren() if i.Name == "Inputs"]
carMakerInputChannelID = carMakerChannelID[0]

# Get NodeID's of CD channels
test3  = nodeIDUtil.IDToCustomDeviceSection(carMakerInputChannelID).GetChildren()
[print("Name3",i.Name,"ID3",i.NodeID,"GUID", i.TypeGUID) for i in test3]
carMakerChannelGUID = [i.TypeGUID for i in test3]
carMakerInputChannelGUID = carMakerChannelGUID[0]

print(len(test3))
# Add Channel to section. Alla kanaler i Iput sektionen har samma GUID
newItem = System.Boolean(False)

#hmm = re.findall("[0-9]","test3")
#aNewChannel = "aNewChannel"+"{}".format()
index = len(test3)+1
indexedChannelName = "myChannel_"+"{}".format(index)
CD_channel, newItem_out  = nodeIDUtil.IDToCustomDeviceSection(carMakerInputChannelID).AddCustomDeviceChannelIfNotFound(indexedChannelName,carMakerInputChannelGUID,newItem)
print(CD_channel.Name)

error = System.String("")
error_out = System.String("")
status, error_out = systemDefinitionObject.SaveSystemDefinitionFile(error)
print(status,error_out)