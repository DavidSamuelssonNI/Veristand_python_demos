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
SystemDefinition_file_Path = System.String("C:\\Users\\dsamuels\\Documents\\VeriStand Projects\\Engine Demo 19\\Engine Demo.nivssdf")
deploy_system_definition = System.Boolean(True)
timeout = System.UInt32(500000)
#Connects the VeriStand Gateway to one or more targets and deploys the system definition file.
# errorCheck = factoryWorkspaceInterface.ConnectToSystem(SystemDefinition_file_Path, deploy_system_definition, timeout)
# print(errorCheck.Code)

#Gets the current state of the system to which the VeriStand Gateway is connected.
#signalArray = System.Array[System.String](["Sig1","Sig2","Sig3"])
stringToReturn1 = System.String("")
stringToReturn2 = System.Array[System.String]([])
stringToReturn1_r = System.String("")
stringToReturn2_r = System.Array[System.String]([])
enumSystemState = SystemState.Active
enumSystemState1 = SystemState.Idle

#print(type(SystemState))
errorCheck,enumSystemState,stringToReturn1_r,stringToReturn2_r = factoryWorkspaceInterface.GetSystemState(enumSystemState,stringToReturn1,stringToReturn2)
print(stringToReturn1_r)