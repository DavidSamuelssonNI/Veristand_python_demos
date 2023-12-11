import clr
import sys
import time
# See figure 124, p.198 in ASAM_AE_XIL_Generic-Simulator-Interface_BS-1-4-Programmers-Guide_V2-1-0.pdf

# Function to add multiple paths to sys.path
def add_paths(*paths):
    for path in paths:
        sys.path.append(path)

# Add necessary paths
add_paths(
r"C:\Windows\Microsoft.NET\assembly\GAC_MSIL\ASAM.XIL.Interfaces\v4.0_2.1.0.0__bf471dff114ae984",
r"c:\Windows\Microsoft.NET\assembly\GAC_MSIL\ASAM.XIL.Implementation.Testbench\v4.0_2.1.0.0__a258c402a414cddb",
r"C:\Windows\Microsoft.NET\assembly\GAC_MSIL\ASAM.XIL.Implementation.Framework\v4.0_2.1.0.0__223668b9b1d3f17b",
r"C:\Windows\Microsoft.NET\assembly\GAC_MSIL\ASAM.XIL.Implementation.XILSupportLibrary\v4.0_2.1.0.0__eb08b67b2f57b9b0",
r"C:\Windows\Microsoft.NET\assembly\GAC_MSIL\ASAM.XIL.Implementation.ManifestReader\v4.0_2.1.0.0__8389d4d3a9402de1",
r"C:\Windows\Microsoft.NET\assembly\GAC_MSIL\ASAM.XIL.Implementation.Testbench\v4.0_2.1.0.0__a258c402a414cddb",
r"C:\Windows\Microsoft.NET\assembly\GAC_MSIL\ASAM.XIL.Implementation.TestbenchFactory\v4.0_2.1.0.0__fc9d65855b27d387"
)

# Add references
clr.AddReference("ASAM.XIL.Interfaces")
clr.AddReference('ASAM.XIL.Implementation.TestbenchFactory')

import ASAM.XIL
from ASAM.XIL.Implementation.TestbenchFactory.Testbench import  TestbenchFactory

# Create TestbenchFactory instance
tbFactory = TestbenchFactory()
print(tbFactory)

# Create Testbench instance
tb = tbFactory.CreateVendorSpecificTestbench("National Instruments", "NI VeriStand ASAM XIL Interface", "2023")
print(tb)

MAPortFactory = ASAM.XIL.Interfaces.Testbench.MAPort.IMAPortFactory(tb.MAPortFactory)
print(MAPortFactory)

# Create MAPort instance
MyMAPort = MAPortFactory.CreateMAPort("NI MAPort 1")
print(MyMAPort)

# Load configuration
config = MyMAPort.LoadConfiguration(r"C:\Users\Public\Documents\National Instruments\NI VeriStand 2023\Examples\DotNet4.6.2\ASAM XIL\Read and Write Channel Values with Model Access Port\PortConfiguration.xml")

print(config)

# Configure MAPort
MyMAPort.Configure(config, True)

# START SIMULATION
MyMAPort.StartSimulation()
time.sleep(2)

# Define a function for writing values
def write_value(port, path, value):
    print(f'Writing Value to {path}:')
    print(value.Value)
    port.Write(path, value)
    time.sleep(1)

def read_value(path):
    ReadVal = MyMAPort.Read(path)
    retFloatVal = ReadVal
    print('Reading Value:')
    print(retFloatVal.Value)

valueFact = tb.ValueFactory
RPM_sp = valueFact.CreateFloatValue(1000)
engine_on = valueFact.CreateFloatValue(1)


# Perform write operations using the defined function
write_value(MyMAPort, "Targets/Controller/Simulation Models/Models/Engine Demo/Inports/command_EngineOn", engine_on)
write_value(MyMAPort, "Targets/Controller/Simulation Models/Models/Engine Demo/Inports/command_RPM", RPM_sp)

# Usage:
read_value("Targets/Controller/Simulation Models/Models/Engine Demo/Parameters/b11")

# ...

# Clean-up
print('Closing')
MyMAPort.StopSimulation()
MyMAPort.Disconnect()
MyMAPort.Dispose()
