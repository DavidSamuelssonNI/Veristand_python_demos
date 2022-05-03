import clr
import sys
import System
from System.Collections import *

sys.path.append("c:\\Program Files (x86)\\National Instruments\\VeriStand 2020 \
                \\nivs.lib\\Reference Assemblies")
clr.AddReference("NationalInstruments.VeriStand.SystemDefinitionAPI")
clr.AddReference("NationalInstruments.VeriStand.ClientAPI")
clr.AddReference("NationalInstruments.VeriStand")

from NationalInstruments.VeriStand.SystemDefinitionAPI import (SystemDefinition,
                                                               Procedure)
from NationalInstruments.VeriStand import Error

systemDefinitionFilePath = (r"C:\Users\dsamuels\Documents\VeriStand Projects"
                            r"\Default Project 3\Default Project 3.nivssdf")
systemDefinitionObject = SystemDefinition(systemDefinitionFilePath)
first_target = systemDefinitionObject.Root.GetTargets().GetTargetList()[0]

def GetProcedures():
    """Get list of procedures 

    Returns:
        List: procedures 
    """

    procedures = first_target.GetProcedures().GetProceduresList()
    #print
    for i in range(len(procedures)):
        print(procedures[i].Name)
        [print("    ",ii.Name) for ii in procedures[i].GetChildren()]
    return procedures


def GetSystemChannels():
    sys_channels = first_target.GetSystemChannels().GetSystemChannels()
    return sys_channels


def AddProcedure(name, desc):
    """Add new item to procedure

    Args:
        name (str): name
        desc (str): description

    Returns:
        procedure_type: if need to add properties
    """
    procedure_object  = Procedure(name, desc)
    first_target.GetProcedures().AddProcedure(procedure_object)
    return procedure_object

# add to a created procedure
def AddProcedureStep():

    procedures = GetProcedures()
    basenode_channel = GetSystemChannels()
    Name = System.String("var3")
    Desc = System.String("desc")
    error = Error()
    value = System.Double(0)
    # I just choose the first ( [0] ) of the procedures and system channels
    # as example
    [success,error] = procedures[0].AddNewSetVariable(Name, 
                                                      Desc,
                                                      basenode_channel[0],
                                                      value, 
                                                      error)

def SaveSysDef():
    error = System.String("")
    error_out = System.String("")
    status, error_out = systemDefinitionObject.SaveSystemDefinitionFile(error)
    print("SystemDefinitionFile Saved with status: ",status,error_out)

if __name__ == "__main__": 

    AddProcedureStep()
    SaveSysDef()

