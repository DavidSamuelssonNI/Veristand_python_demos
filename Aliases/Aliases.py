import csv
import clr
import sys
import System
import time
import argparse
import shutil
import logging
import os
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

    def add_aliases(self):

        ## Cust device
        # CD - Map1 (Childx1) list of Map1
        #          map2 (Childx2) list of Map2, (Map1()[x]) x = map to get list of
        #               map3 (childx3) list of Map3, (Map2()[x]) x = map to get list of
        test3 = self._first_target.GetCustomDevices().GetCustomDeviceList()[0].GetChildren()
        [print("Test3: ", i.Name,i.Description ) for i in test3]
        test4 = self._first_target.GetCustomDevices().GetCustomDeviceList()[0].GetChildren()[1].GetChildren()
        [print("Test4: ", i.Name, ) for i in test4]
        test5 = self._first_target.GetCustomDevices().GetCustomDeviceList()[0].GetChildren()[1].GetChildren()[0].GetChildren()
        [print("Test5: ", i.Name, i.NodePath ) for i in test5]

        error = Error()
        error_out = Error()
        success =  System.Boolean(False)
        CD_folder_name_1 = System.String(test3[1].Name)
        CD_folder_name_2 = System.String(test3[2].Name)
        CD_folder_desc_1 = System.String(test3[1].Description)
        CD_folder_desc_2 = System.String(test3[2].Description)
        print("sgda",not str(CD_folder_desc_1).strip()) #string empty or only whitespaces
        print("DESC:{}".format(CD_folder_name_1), "DESC:{}".format(CD_folder_name_2))
        print("DESC:{}".format(CD_folder_desc_1), "DESC:{}".format(CD_folder_desc_2))
        # Add alias
        aliases = self._system_definition_object.Root.GetAliases().GetAliasesList()
        [print("Aliases: ", i.Name, i.NodePath) for i in aliases]
        alias_folder_1 = AliasFolder(CD_folder_name_1,"test")
        alias_folder_2 = AliasFolder(CD_folder_name_2,"test")
        success, error_out = self._system_definition_object.Root.GetAliases().AddAliasFolder(alias_folder_1,error)
        print(success,error)
        success, error_out = self._system_definition_object.Root.GetAliases().AddAliasFolder(alias_folder_2,error)

        cdname = System.Array[System.String]([])
        cdvalue = System.Array[System.Double]([])
        # test6  = self._first_target.GetCustomDevices().GetCustomDeviceList()[0].GetChildren()
        # #test6 = [i.NodeID for i in customDevices_objects if i.Name == "CarMaker"]
        # [print("sdg: ",i.Name, i.NodeID, i.NodePath) for i in test6]

        nodeIDUtil = NodeIDUtil()
        custom_devices = self._first_target.GetCustomDevices().GetCustomDeviceList()
        [print("CustomDeviceName: ", i.Name, "NodeID: ", i.NodeID,"BaseNodeType: ", i.BaseNodeType) for i in custom_devices]
        
        custom_device_vcom = [i.NodeID for i in custom_devices if i.Name == "VCOM"]
        custom_device_vcom_id = custom_device_vcom[0]
        
        custom_device_channel_list = nodeIDUtil.IDToCustomDeviceSection(custom_device_vcom_id).GetChildren()
        [print("CustomDeviceChan: ", i.Name, "NodeID: ", i.NodeID,"BaseNodeType: ", i.BaseNodeType) for i in custom_device_channel_list]
        custom_device_channel_list_2 = nodeIDUtil.IDToCustomDeviceSection(custom_device_vcom_id).GetChildren()[1].GetChildren()
        [print("CustomDeviceChan2: ", i.Name, "NodeID: ", i.NodeID,"BaseNodeType: ", i.BaseNodeType) for i in custom_device_channel_list_2]
        #Can frame
        custom_device_channel_list_3 = nodeIDUtil.IDToCustomDeviceSection(custom_device_vcom_id).GetChildren()[1].GetChildren()[0].GetChildren()
        [print("CustomDeviceChan3: ", i.Name, "NodeID: ", i.NodeID,"BaseNodeType: ", i.BaseNodeType) for i in custom_device_channel_list_3]
        #Custom device channel ids
        custom_device_channel_list_4 = nodeIDUtil.IDToCustomDeviceSection(custom_device_vcom_id).GetChildren()[1].GetChildren()[0].GetChildren()[0].GetChildren()
        [print("CustomDeviceChan4: ", i.Name, "NodeID: ", i.NodeID,"BaseNodeType: ", i.BaseNodeType) for i in custom_device_channel_list_4]
        #test id
        # hmm = System.UInt64(36)
        # custom_device_channel_obj = nodeIDUtil.IDToCustomDeviceChannel(hmm)

        # error_out = self._system_definition_object.Root.GetAliases().AddNewAliasByReference("name","desc",custom_device_channel_obj,error)
        # print("error_out", error_out)

        myalias = Alias("name","desc",custom_device_channel_list_4[0].NodePath)
        success, error_out = self._system_definition_object.Root.GetAliases().AddAlias(myalias,error)
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
    aliasObject.add_aliases()

    # print("Copied file: {}".format(dst), "\n")
    # print("inputted file: {}".format(args.SysDef), "\n")
    # C:\Users\User\Documents\VeriStand Projects\Test
