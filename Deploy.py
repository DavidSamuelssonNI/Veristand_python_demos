import clr

import sys
import System
import time

sys.path.append("c:\\Program Files (x86)\\National Instruments\\VeriStand 2020\\nivs.lib\\Reference Assemblies")
clr.AddReference("NationalInstruments.VeriStand.SystemDefinitionAPI")
clr.AddReference("NationalInstruments.VeriStand.ClientAPI")
clr.AddReference("NationalInstruments.VeriStand")

from NationalInstruments.VeriStand.SystemDefinitionAPI import SystemDefinition, Database, CANPort, XNETDatabases, SignalBasedFrame
from NationalInstruments.VeriStand.ClientAPI import Factory
from NationalInstruments.VeriStand import Error

#Factory provides access to the NI VeriStand system and the various interfaces available in the Execution API
factory = Factory()

#Interface to perform basic workspace operations, such as getting, setting, and logging channel data. 
factoryWorkspaceInterface = factory.GetIWorkspace2('localhost')

