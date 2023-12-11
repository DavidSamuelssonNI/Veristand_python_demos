import clr
import sys
import time
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
    r"C:\Windows\Microsoft.NET\assembly\GAC_MSIL\ASAM.XIL.Implementation.TestbenchFactory\v4.0_2.1.0.0__fc9d65855b27d387"
)

# Add references
clr.AddReference("ASAM.XIL.Interfaces")
clr.AddReference("ASAM.XIL.Implementation.Testbench")
clr.AddReference("ASAM.XIL.Implementation.Framework")
clr.AddReference("ASAM.XIL.Implementation.XILSupportLibrary")
clr.AddReference("ASAM.XIL.Implementation.ManifestReader")
clr.AddReference("ASAM.XIL.Implementation.TestbenchFactory")

# Check NameSpace of dll:s to evaluate import modules paths
import ASAM.XIL.Interfaces
from ASAM.XIL.Interfaces.Framework.Variables import IFloatVariable
from ASAM.XIL.Interfaces.Testbench.Common.ValueContainer import IFloatValue
from ASAM.XIL.Interfaces.Testbench.Common.ValueContainer import IBaseValue
from ASAM.XIL.Implementation.TestbenchFactory.Testbench import TestbenchFactory
from ASAM.XIL.Implementation.TestbenchFactory.Testbench import TestbenchInfo

PORT_NAME = "MyMaPort"
RPM = 5000
START_ENGINE = 1

# See ASAM_AE_XIL_Generic-Simulator-Interface_BS-1-4-Programmers-Guide_V2-1-0, Fig 124, p.198
def factory(port_name: str) -> object:
    # Create TestbenchFactory instance
    tb_factory = TestbenchFactory()
    logging.info('tb_factory created')

    # Create Testbench instance
    tb = tb_factory.CreateVendorSpecificTestbench("National Instruments", "NI VeriStand ASAM XIL Interface", "2023")
    logging.info('tb instance created')

    MA_Port_Factory = ASAM.XIL.Interfaces.Testbench.MAPort.IMAPortFactory(tb.MAPortFactory)
    logging.info('MA_factory created')

    # Create MAPort instance
    my_MA_port = MA_Port_Factory.CreateMAPort(port_name)
    logging.info('MA instance created')

    # Load configuration
    config = my_MA_port.LoadConfiguration(r"C:\Users\Public\Documents\National Instruments\NI VeriStand 2023\Examples\DotNet4.6.2\ASAM XIL\Read and Write Channel Values with Model Access Port\PortConfiguration.xml")
    logging.info('Configuration loaded')

    # Configure MAPort
    my_MA_port.Configure(config, True)
    logging.info('returned MA_port + Value_factory')
    return my_MA_port, tb.ValueFactory

my_MA_port, value_fact = factory(PORT_NAME)

# START SIMULATION
my_MA_port.StartSimulation()
time.sleep(2)

# Define a function for writing values
def write_value(port, path, value):
    logging.info(f'Writing Value to {path}:')
    logging.info("%f", value.Value)
    port.Write(path, value)
    time.sleep(1)

def read_value(path: str) -> float:
    read_var = my_MA_port.Read(path)
    logging.info("%f", IFloatValue(read_var).Value)
    return IFloatValue(read_var).Value

RPM_sp = value_fact.CreateFloatValue(RPM)
engine_on = value_fact.CreateFloatValue(START_ENGINE)

# Perform write operations using the defined function
write_value(my_MA_port, "Targets/Controller/Simulation Models/Models/Engine Demo/Inports/command_EngineOn", engine_on)
write_value(my_MA_port, "Targets/Controller/Simulation Models/Models/Engine Demo/Inports/command_RPM", RPM_sp)

# Read values 
while(read_value("Aliases/ActualRPM") < RPM_sp.Value):
    time.sleep(1)

# Clean-up
print('Closing')
my_MA_port.StopSimulation()
my_MA_port.Disconnect()
my_MA_port.Dispose()
