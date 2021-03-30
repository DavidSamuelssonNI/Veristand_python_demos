import clr
import sys
import System
import time

'''Run C:\\Users\\Public\\Documents\\National Instruments\\NI VeriStand 2020\\Examples\\Stimulus Profile\\Engine Demo 5\\Engine Demo 5.nivsproj'''

sys.path.append("c:\\Program Files (x86)\\National Instruments\\VeriStand 2020\\nivs.lib\\Reference Assemblies")
clr.AddReference("NationalInstruments.VeriStand.ClientAPI")

from NationalInstruments.VeriStand.ClientAPI import Factory

#Instance of Class Factory provides access to the NI VeriStand system
fac = Factory()
print(fac)

#Interface to perform basic workspace operations
facWork = fac.GetIWorkspace2('localhost')
print(facWork)

#define in out parameters
chan = System.String("Targets/Controller/Simulation Models/Models/Engine Demo/Outports/RPM")
chan2 = System.String("Targets/Controller/Simulation Models/Models/Engine Demo/Inports/command_RPM")
chan = System.String("Targets/CRio/Hardware/Chassis/NI-XNET/CAN/CRIOCAN/Incoming/Single-Point/CANCyclicFrame1 (64)/CANCyclicFrame1 (0,8)")
# chan2 = System.String("Targets/Controller/Simulation Models/Models/Engine Demo/Inports/command_RPM")
out = System.Double(0)
command_RPM =  System.Double(1500)


facWork.SetSingleChannelValue(chan2, command_RPM)
time.sleep(3)
error, out = facWork.GetSingleChannelValue(chan, out)
print("")
print("Error code:")
print(error.get_Code())
print("Channel name:")
print(chan)
print("Channel Value:")
print(out)

