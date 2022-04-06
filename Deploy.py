import clr
import sys
import System
import time
from System.Collections import *

sys.path.append("c:\\Program Files (x86)\\National Instruments\\VeriStand 2020\\nivs.lib\\Reference Assemblies")
clr.AddReference("NationalInstruments.VeriStand.SystemDefinitionAPI")
clr.AddReference("NationalInstruments.VeriStand.ClientAPI")
clr.AddReference("NationalInstruments.VeriStand")

from NationalInstruments.VeriStand.SystemDefinitionAPI import SystemDefinition, Database, CANPort, XNETDatabases, SignalBasedFrame
from NationalInstruments.VeriStand.ClientAPI import Factory, SystemState
from NationalInstruments.VeriStand import Error

errorCheck = Error()

#Factory provides access to the NI VeriStand system and the various interfaces available in the Execution API
factory = Factory()

#Interface to perform basic workspace operations, such as getting, setting, and logging channel data.
factoryWorkspaceInterface = factory.GetIWorkspace2('localhost')

#SystemDefinition
SystemDefinitionFilePath = System.String("C:\\Users\\dsamuels\\Documents\\VeriStand Projects\\Engine Demo 20\\Engine Demo.nivssdf")
#SystemDefinitionFilePath = r"C:\Users\dsamuels\Documents\VeriStand Projects\Engine Demo 20\Engine Demo.nivssdf"
print(SystemDefinitionFilePath)

deploySystemDefinition = System.Boolean(True)
timeout = System.UInt32(500000)
#Connects the VeriStand Gateway to one or more targets and deploys the system definition file.
errorCheck = factoryWorkspaceInterface.ConnectToSystem(SystemDefinitionFilePath, deploySystemDefinition, timeout)
print(errorCheck.Code)

#Gets the current state of the system to which the VeriStand Gateway is connected.
#signalArray = System.Array[System.String](["Sig1","Sig2","Sig3"])
systemDefinitionFile = System.String("")
targets = System.Array[System.String]([])
systemDefinitionFile_retured = System.String("")
targets_returned = System.Array[System.String]([])
enumSystemState = SystemState.Active
enumSystemState1 = SystemState.Idle

#print(type(SystemState))
errorCheck,enumSystemState,systemDefinitionFile_retured,targets_returned = factoryWorkspaceInterface.GetSystemState(enumSystemState, systemDefinitionFile, targets)
print("Status getSystemState,error: ", errorCheck)
print("Status getSystemState,SystemState status: ", enumSystemState)
print("Status getSystemState,SystemDefinitionFile Loaded : ", systemDefinitionFile_retured)
for i in targets_returned:
    print("Status getSystemState,Current-Target: ", i)

