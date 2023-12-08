import clr
import sys
import time

# Function to add multiple paths to sys.path
def add_paths(*paths):
    for path in paths:
        sys.path.append(path)

# Add necessary paths
add_paths(
    "C:\\Windows\\Microsoft.NET\\assembly\\GAC_MSIL\\ASAM.XIL.Interfaces\\v4.0_2.1.0.0__bf471dff114ae984",
    "c:\\Windows\\Microsoft.NET\\assembly\\GAC_MSIL\\ASAM.XIL.Implementation.Testbench\\v4.0_2.1.0.0__a258c402a414cddb",
    # Add other paths here...
)

# Add references
clr.AddReference("ASAM.XIL.Interfaces")
clr.AddReference('ASAM.XIL.Implementation.TestbenchFactory')

from ASAM.XIL.Implementation.TestbenchFactory.Testbench import TestbenchFactory

# Create TestbenchFactory instance
tbFactory = TestbenchFactory()
print(tbFactory)

# Create Testbench instance
tb = tbFactory.CreateVendorSpecificTestbench("National Instruments", "NI VeriStand ASAM XIL Interface", "2020")
print(tb)

maportFactory = ASAM.XIL.Interfaces.Testbench.MAPort.IMAPortFactory(tb.MAPortFactory)
print(maportFactory)

# Create MAPort instance
MyMAPort = maportFactory.CreateMAPort("NI MAPort 1")
print(MyMAPort)

# Load configuration
config = MyMAPort.LoadConfiguration("c:\\Users\\Public\\Documents\\National Instruments\\NI VeriStand 2020\\Examples\\Stimulus Profile\\Engine Demo\\MAPortConfig.xml")
print(config)

# Configure MAPort
MyMAPort.Configure(config, 1)

# START SIMULATION
MyMAPort.StartSimulation()
time.sleep(2)

# Write and Read operations...

# Example structure:

def read_value(path):
    ReadVal = MyMAPort.Read(path)
    retFloatVal = ReadVal
    print('Reading Value:')
    print(retFloatVal.Value)

# Usage:
read_value("Targets/Controller/Simulation Models/Models/Engine Demo/Parameters/b11")

# ...

# Clean-up
print('Closing')
MyMAPort.StopSimulation()
MyMAPort.Disconnect()
MyMAPort.Dispose()
