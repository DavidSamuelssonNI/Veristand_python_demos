import clr

import sys
import System
import time

sys.path.append("c:\\Program Files (x86)\\National Instruments\\VeriStand 2020\\nivs.lib\\Reference Assemblies")
clr.AddReference("NationalInstruments.VeriStand.SystemDefinitionAPI")
clr.AddReference("NationalInstruments.VeriStand")
from NationalInstruments.VeriStand.SystemDefinitionAPI import SystemDefinition, Database, CANPort, XNETDatabases, SignalBasedFrame
from NationalInstruments.VeriStand import Error

xnetSysDef = SystemDefinition("C:\\Users\\dsamuels\\Documents\\VeriStand Projects\\Engine Demo 8\\Engine Demo.nivssdf")
print(xnetSysDef)
firstTarget = xnetSysDef.Root.GetTargets().GetTargetList()[0]
print(firstTarget)
canSection = firstTarget.GetHardware().GetChassisList()[0].GetXNET().GetCAN()
print(canSection)

# canSection.GetCANPortList()[0].RemoveNode()

NIXNET_example = Database("test")

# yryd = firstTarget.GetXNETDatabases().GetDatabaseList()
# print(yryd[0])


portName = System.String("CAN1")
portNumber = System.UInt16(1)
clusterName = System.String("CAN_Cluster")
baudRate = System.UInt32(500000)

# Create a CAN port associated with a cluster in the database you opened
car1CANPort = CANPort(portName, portNumber, NIXNET_example, clusterName, baudRate)

#Get the Single-Point Frame section that appears under the new CANPort
singlePointSection = car1CANPort.GetIncoming().GetSinglePoint()
print(singlePointSection)




#Add a frame to the database

frameName = System.String("Frame1")
testa = System.String("Frame1")
frameID = System.UInt32(32)
frameClusterName = System.String("CAN_Cluster")
framPayloadLength = System.UInt32(8)
frameOffset = System.Double(-1)
frameEnable64 = System.Boolean(False)
signalArray = System.Array[System.String](["Sig1","Sig2","Sig3"])
error = Error()
singlePointSection.AddSignalBasedFrame(SignalBasedFrame(frameName,frameID,NIXNET_example,frameClusterName,framPayloadLength,frameOffset,frameEnable64,signalArray),error)
print(error.ErrorCode)
canSection.AddCANPort(car1CANPort)

error = System.String("")
path = System.String("C:\\Users\\dsamuels\\Documents\\VeriStand Projects\\Engine Demo 8\\Engine Demo.nivssdf")
xnetSysDef.SaveSystemDefinitionFile(path,error)
#SystemDefinition xnetSysDef = new SystemDefinition("C:\\Users\\Public\\Public Documents\\National Instruments\\NI VeriStand 2012\\Projects\\XNETAPIExample\\XNETAPIExample.nivssdf");