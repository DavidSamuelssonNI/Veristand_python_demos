import csv
import clr
import sys
import System
import time
import argparse
import shutil
import logging
import os
from enum import Enum
from System.Collections import *

sys.path.append("c:\\Program Files\\National Instruments\\VeriStand 2023\\nivs.lib\\Reference Assemblies")
clr.AddReference("NationalInstruments.VeriStand.SystemDefinitionAPI")
clr.AddReference("NationalInstruments.VeriStand.ClientAPI")
clr.AddReference("NationalInstruments.VeriStand")

from NationalInstruments.VeriStand.SystemDefinitionAPI import SystemDefinition, Alias, Aliases, AliasFolder, NodeIDUtil
from NationalInstruments.VeriStand.ClientAPI import Factory, SystemState
from NationalInstruments.VeriStand import Error

current_dir = os.path.dirname(__file__)
# See http://pythonnet.github.io/ for PyhtonNet documentation


class AliasController:
    def __init__(self):
        self._system_definition_object = None
        self._first_target = None

    def create_system_definition_src(self, ip_address_in = '192.168.0.3', data_rate_in = 1000):
        """
        Create a system definition from source and set properties.
        """
        logging.info("Creating System Definition from source")
        name = System.String("Name")
        description = System.String("Description")
        creator = System.String("Creator")
        version = System.String("1")
        target_name = System.String("MyController")
        target_type = System.String("Linux_x64")
        filepath = System.String(os.path.join(current_dir, "apadef.nivssdf"))
        # ip_address = System.String(ip_address_in)
        # data_rate = System.Double(data_rate_in)

        try:
            self._system_definition_object = SystemDefinition(name, description, creator, version, target_name, target_type, filepath)
            self._first_target = self._system_definition_object.Root.GetTargets().GetTargetList()[0]

            # Set properties
            self._first_target.IPAddress = ip_address_in # ip_address
            self._first_target.TargetRate = data_rate_in # data_rate

            self.SaveSystemDefinition()
        except Exception as e:
            logging.error(f"Error creating system definition: {e}")
    
    def create_system_definition(self,path):
        """
        Create a system definition and set properties.
        """
        logging.info("Creating System Definition")
        ip_address = System.String("192.168.0.3")
        data_rate = System.Double(1000)
        target_type = System.String("Linux_x64")
        try:
            self._system_definition_object = SystemDefinition(path)
            self._first_target = self._system_definition_object.Root.GetTargets().GetTargetList()[0]

            # Set properties
            self._first_target.IPAddress = ip_address # ip_address
            self._first_target.TargetRate = data_rate # data_rate

            self.SaveSystemDefinition()
        except Exception as e:
            logging.error(f"Error creating system definition: {e}")

    def SaveSystemDefinition(self):
        # Save SystemDefinitionFile
        error = System.String("")
        error_out = System.String("")
        functionReturn, error_out = self._system_definition_object.SaveSystemDefinitionFile(error)

        if (not error_out):
            print("File saved")
        else:
            print(error_out)

    def add_aliases_folder(self):
        error = Error()
        error_out = Error()
        success =  System.Boolean(False)

        ECU = self._first_target.GetCustomDevices().GetCustomDeviceList()[0].GetChildren()
        [print("ECU: ", i.Name,i.Description ) for i in ECU]
        frames = self._first_target.GetCustomDevices().GetCustomDeviceList()[0].GetChildren()[1].GetChildren()
        [print("frames: ", i.Name, ) for i in frames]
        CAN_messages = self._first_target.GetCustomDevices().GetCustomDeviceList()[0].GetChildren()[1].GetChildren()[0].GetChildren()
        [print("CAN_messages: ", i.Name, i.NodePath ) for i in CAN_messages]

        CD_folder_name_1 = System.String(ECU[1].Name) 
        CD_folder_name_2 = System.String(ECU[2].Name)
        CD_folder_desc_1 = System.String(ECU[1].Description)
        CD_folder_desc_2 = System.String(ECU[2].Description)
        #print("sgda",not str(CD_folder_desc_1).strip()) #string empty or only whitespaces
        print("DESC:{}".format(CD_folder_name_1), "DESC:{}".format(CD_folder_name_2))
        print("DESC:{}".format(CD_folder_desc_1), "DESC:{}".format(CD_folder_desc_2))

        aliases = self._system_definition_object.Root.GetAliases().GetAliasesList()
        [print("Aliases: ", i.Name, i.NodePath) for i in aliases]
        alias_folder_1 = AliasFolder(CD_folder_name_1,"test")
        alias_folder_2 = AliasFolder(CD_folder_name_2,"test")
        success, error_out = self._system_definition_object.Root.GetAliases().AddAliasFolder(alias_folder_1,error)
        print(success,error)
        success, error_out = self._system_definition_object.Root.GetAliases().AddAliasFolder(alias_folder_2,error)

    def add_aliases(self):
        error = Error()
        error_out = Error()
        success =  System.Boolean(False)
        nodeIDUtil = NodeIDUtil()
        custom_devices = self._first_target.GetCustomDevices().GetCustomDeviceList()
        custom_device_vcom = [i.NodeID for i in custom_devices if i.Name == "VCOM"]
        custom_device_vcom_id = custom_device_vcom[0]


        ECU_Status = 0
        ECU_ADAS = 1
        ECU_DAQ = 2
        FRAMES = 0 # only one list of frames per ECU
        CAN_MESSAGE = 0

        #ta length av ECU,CAN_message och signals

        ECU = nodeIDUtil.IDToCustomDeviceSection(custom_device_vcom_id).GetChildren()
        [print("ECU: ", i.Name, "NodeID: ", i.NodeID,"BaseNodeType: ", i.BaseNodeType) for i in ECU]
        frames = nodeIDUtil.IDToCustomDeviceSection(custom_device_vcom_id).GetChildren()[ECU_ADAS].GetChildren()
        [print("frames: ", i.Name, "NodeID: ", i.NodeID,"BaseNodeType: ", i.BaseNodeType) for i in frames]
        #Can frame
        CAN_message = nodeIDUtil.IDToCustomDeviceSection(custom_device_vcom_id).GetChildren()[ECU_ADAS].GetChildren()[FRAMES].GetChildren()
        [print("CAN_message: ", i.Name, "NodeID: ", i.NodeID,"BaseNodeType: ", i.BaseNodeType) for i in CAN_message]
        #Custom device channel ids
        signals = nodeIDUtil.IDToCustomDeviceSection(custom_device_vcom_id).GetChildren()[ECU_ADAS].GetChildren()[FRAMES].GetChildren()[CAN_MESSAGE].GetChildren()
        nr_of_signals = len(signals)
        print(nr_of_signals)
        [print("signals: ", i.Name, "NodeID: ", i.NodeID,"BaseNodeType: ", i.BaseNodeType) for i in signals]
        #save to matrix list or dictionary or something

        #loop over
        for sig in signals:
            myalias = Alias(sig.Name,sig.NodePath,sig.NodePath)
            success, error_out = self._system_definition_object.Root.GetAliases().AddAlias(myalias,error)
            success, error_out = self._system_definition_object.Root.GetAliases().GetAliasFolderList()[1].AddAlias(myalias,error) # add to folder
        print(success,error_out)
        self.SaveSystemDefinition()
        #går det att använda en custom_device_channel_obj i AddNewAliasByReference? stödjer den den typen?


if __name__ == "__main__":

    aliasObject = AliasController()
    
    parser = argparse.ArgumentParser(description='SysDef to be processed')
    parser.add_argument('--SysDef',
                        metavar='FILE_PATH',
                        type=str,
                        action='store',
                        help='Path+name of file to append to')
    args = parser.parse_args()

    dst = r"C:\Users\User\Documents\VeriStand Projects\Test\Test_copy.nivssdf"
    shutil.copyfile(args.SysDef, dst)
    
    aliasObject.create_system_definition(args.SysDef)
    aliasObject.add_aliases_folder()
    aliasObject.add_aliases()

    # print("Copied file: {}".format(dst), "\n")
    # print("inputted file: {}".format(args.SysDef), "\n")
    # C:\Users\User\Documents\VeriStand Projects\Test
