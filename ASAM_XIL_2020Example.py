import clr
import sys
import System

import os
import winreg
import time

sys.path.append("C:\\Windows\\Microsoft.NET\\assembly\\GAC_MSIL\\ASAM.XIL.Interfaces\\v4.0_2.1.0.0__bf471dff114ae984")

sys.path.append("c:\\Windows\\Microsoft.NET\\assembly\\GAC_MSIL\\ASAM.XIL.Implementation.Testbench\\v4.0_2.1.0.0__a258c402a414cddb")
sys.path.append("C:\\Windows\\Microsoft.NET\\assembly\\GAC_MSIL\\ASAM.XIL.Implementation.Framework\\v4.0_2.1.0.0__223668b9b1d3f17b")
sys.path.append("C:\\Windows\\Microsoft.NET\\assembly\\GAC_MSIL\\ASAM.XIL.Implementation.XILSupportLibrary\\v4.0_2.1.0.0__eb08b67b2f57b9b0")
sys.path.append("C:\\Windows\\Microsoft.NET\\assembly\\GAC_MSIL\\ASAM.XIL.Implementation.ManifestReader\\v4.0_2.1.0.0__8389d4d3a9402de1")
sys.path.append("C:\\Windows\\Microsoft.NET\\assembly\\GAC_MSIL\\ASAM.XIL.Implementation.Testbench\\v4.0_2.1.0.0__a258c402a414cddb")
sys.path.append("C:\\Windows\\Microsoft.NET\\assembly\\GAC_MSIL\\ASAM.XIL.Implementation.TestbenchFactory\\v4.0_2.1.0.0__fc9d65855b27d387")

clr.AddReference("ASAM.XIL.Interfaces")
clr.AddReference('ASAM.XIL.Implementation.TestbenchFactory')

import ASAM.XIL
from ASAM.XIL.Implementation.TestbenchFactory.Testbench import TestbenchFactory

tbFactory = TestbenchFactory()
print(tbFactory)

tb = tbFactory.CreateVendorSpecificTestbench("National Instruments", "NI VeriStand ASAM XIL Interface", "2020")
print(tb)

maportFactory = ASAM.XIL.Interfaces.Testbench.MAPort.IMAPortFactory(tb.MAPortFactory)
print(maportFactory)

MyMAPort = maportFactory.CreateMAPort("NI MAPort 1")
print(MyMAPort)

config = MyMAPort.LoadConfiguration("c:\\Users\\Public\\Documents\\National Instruments\\NI VeriStand 2020\\Examples\\Stimulus Profile\\Engine Demo\\MAPortConfig.xml")
print(config)

MyMAPort.Configure(config, 1)

#START SIMULATION
MyMAPort.StartSimulation()
time.sleep(2)

valueFact = tb.ValueFactory
writeVal = valueFact.CreateFloatValue(1000)
writeVal2 = valueFact.CreateFloatValue(1)

print('Reading Value:')
ReadVal = MyMAPort.Read("Targets/Controller/Simulation Models/Models/Engine Demo/Parameters/b11")
retFloatVal = ReadVal
print(retFloatVal.Value)

###
print('Writing Value, EngineOn:')
print(writeVal2.Value)

MyMAPort.Write("Targets/Controller/Simulation Models/Models/Engine Demo/Inports/command_EngineOn", writeVal2)
time.sleep(1)
###

print('Writing Value, RPMSetpoint:')
print(writeVal.Value)

MyMAPort.Write("Targets/Controller/Simulation Models/Models/Engine Demo/Inports/command_RPM", writeVal)
time.sleep(1)

NewReadVal = MyMAPort.Read("Targets/Controller/Simulation Models/Models/Engine Demo/Parameters/b11")
print('Reading Value:')
print(NewReadVal.Value)

print('Sleep 15s')
time.sleep(15)

print('Closing')
MyMAPort.StopSimulation()
MyMAPort.Disconnect()
MyMAPort.Dispose()

