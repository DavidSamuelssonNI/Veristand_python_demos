
import clr
import sys
import System
import time

from System import *
from System.Collections import *

sys.path.append("c:\\Program Files (x86)\\National Instruments\\VeriStand 2020\\nivs.lib\\Reference Assemblies")
clr.AddReference("NationalInstruments.VeriStand.SystemDefinitionAPI")
clr.AddReference("NationalInstruments.VeriStand.ClientAPI")
clr.AddReference("NationalInstruments.VeriStand")

from NationalInstruments.VeriStand.SystemDefinitionAPI import SystemDefinition, Database, CANPort, XNETDatabases, SignalBasedFrame
from NationalInstruments.VeriStand.ClientAPI import Factory, SystemState
from NationalInstruments.VeriStand import Error

#Factory provides access to the NI VeriStand system and the various interfaces available in the Execution API
factory = Factory()
errorCheck = Error()

#Get interface that contains the sendMessage() method
systemDefinitionFilePath = r"C:\Users\dsamuels\Documents\VeriStand Projects\Engine Demo 20\Engine Demo.nivssdf"
gatewayIpAdress = 'localhost'
ICustomDevice = factory.GetICustomDevice(gatewayIpAdress, systemDefinitionFilePath)

#Common to both sendMessage() methods
command = System.String("TransmitData")

#sendMessage using Bytes
returnedResponse = System.Array[System.Byte]([])
response = System.Array[System.Byte]([])
bytesIn = System.Array[System.Byte]([2])
timeout = System.UInt32(0)

#sendMessage using Strings
data = System.String("")
resp_out = System.String("")
resp = System.String("")

#sendMessage() using Bytes
errorCheck,returnedResponse = ICustomDevice.SendMessage(command,bytesIn,timeout,response)

#sendMessage() using Strings
#errorCheck,resp = ICustomDevice.SendMessage(command,data,timeout,resp_out)

print(errorCheck.IsError)
print(int(errorCheck.Code))
print(errorCheck.ResolvedErrorMessage)


