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
# Configure the logging system

log_filename = "my_log_file.log"

# Set the logging level to control which messages are recorded in the log file
logging.basicConfig(
    level=logging.INFO,  # Set the minimum level to INFO
    filename=log_filename,  # Specify the log file name
    filemode="a",  # Append to the log file
    format="%(asctime)s [%(levelname)s]: %(message)s",  # Log message format
)

class AliasController:
    def __init__(self):
        self._system_definition_object = None
        self._first_target = None
        self.error = Error()
        self.error_out = Error()
        self.success =  System.Boolean(False)
        #For Custom device references
        self.nodeIDUtil = NodeIDUtil()

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

            self.save_system_definition()
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
            self._first_target.OperatingSystem = target_type
            self.save_system_definition()
        except Exception as e:
            logging.error(f"Error creating system definition: {e}")

    def save_system_definition(self):
        """
        Save the system definition file
        """
        error = System.String("")
        error_out = System.String("")
        functionReturn, error_out = self._system_definition_object.SaveSystemDefinitionFile(error)

        if (not error_out):
            log = "File saved"
        else:
            log = error_out
        logging.info(log)

    def add_aliases_folder(self):
        """
        Add aliases folder using GetCustomDevices 
        """
        ECU = self._first_target.GetCustomDevices().GetCustomDeviceList()[0].GetChildren()
        frames = self._first_target.GetCustomDevices().GetCustomDeviceList()[0].GetChildren()[1].GetChildren()
        CAN_messages = self._first_target.GetCustomDevices().GetCustomDeviceList()[0].GetChildren()[1].GetChildren()[0].GetChildren()


        CD_folder_name_1 = System.String(ECU[1].Name) 
        CD_folder_name_2 = System.String(ECU[2].Name)
        CD_folder_desc_1 = System.String(ECU[1].Description)
        CD_folder_desc_2 = System.String(ECU[2].Description)
        #print("sgda",not str(CD_folder_desc_1).strip()) #string empty or only whitespaces

        aliases = self._system_definition_object.Root.GetAliases().GetAliasesList()

        alias_folder_1 = AliasFolder(CD_folder_name_1,"test")
        alias_folder_2 = AliasFolder(CD_folder_name_2,"test")
        success, self.error_out = self._system_definition_object.Root.GetAliases().AddAliasFolder(alias_folder_1,self.error)
        success, self.error_out = self._system_definition_object.Root.GetAliases().AddAliasFolder(alias_folder_2,self.error)
        logging.info("Alias folders created successfully")

    def add_aliases(self):
        """
        Add aliases using custom device references IDToCustomDeviceSection
        """
        logging.info("Adding aliases")
        custom_devices = self._first_target.GetCustomDevices().GetCustomDeviceList()
        custom_device_vcom = [i.NodeID for i in custom_devices if i.Name == "VCOM"]
        custom_device_vcom_id = custom_device_vcom[0]

        class ECU(Enum):
            Status = 0
            ADAS = 1
            DAQ = 2

        for ECU_index, ECU_value in enumerate(self.nodeIDUtil.IDToCustomDeviceSection(custom_device_vcom_id).GetChildren()):
            if ECU_index > 0:
                for frames_index, frames_value in enumerate(ECU_value.GetChildren()):
                    for CAN_message_index, CAN_message_value in enumerate(frames_value.GetChildren()):
                        for signals in CAN_message_value.GetChildren():
                            ECU_name = ECU_value.Name
                            frame_name = frames_value.Name
                            CAN_message_name = CAN_message_value.Name
                            signal_name = signals.Name

                            logging.info("ECU: {}, Frame: {}, CAN_Message: {}, SignalName: {}".format(ECU_name, frame_name, CAN_message_name, signal_name))

                            write_alias = Alias(signal_name, signals.NodePath, signals.NodePath)

                            if ECU_index == ECU.ADAS.value:
                                # folder_index = ECU_index - 1
                                folder_index = 3 # Hardcoded for Close loop Control Example - ADAS.nivssdf_copy
                                success, error_out = self._system_definition_object.Root.GetAliases().GetAliasFolderList()[folder_index].AddAlias(write_alias, self.error)
                                log = "ADAS aliases printed" 
                                logging.info("ADAS aliases printed {} {}".format(success, error_out))
                            elif ECU_index == ECU.DAQ.value:
                                # folder_index = ECU_index - 1
                                folder_index = 4 # Hardcoded for Close loop Control Example - ADAS.nivssdf_copy
                                success, error_out = self._system_definition_object.Root.GetAliases().GetAliasFolderList()[folder_index].AddAlias(write_alias, self.error)
                                log = "DAQ aliases printed"
                            logging.info("{} {} {}".format(log, success, error_out))

        self.save_system_definition()


if __name__ == "__main__":

    aliasObject = AliasController()
    
    parser = argparse.ArgumentParser(description='SysDef to be processed')
    parser.add_argument('--SysDef',
                        metavar='FILE_PATH',
                        type=str,
                        action='store',
                        help='Path+name of file to append to')
    args = parser.parse_args()

    # dst = r"C:\Users\User\Documents\VeriStand Projects\Test\Test_copy.nivssdf"
    dst = r"C:\Users\User\Documents\VeriStand Projects\Veristand 2023 Q4\Veristand 2023 Q4\Close loop Control Example - ADAS\Close loop Control Example - ADAS.nivssdf_copy"
    shutil.copyfile(args.SysDef, dst)
    
    aliasObject.create_system_definition(args.SysDef)
    aliasObject.add_aliases_folder()
    aliasObject.add_aliases()

