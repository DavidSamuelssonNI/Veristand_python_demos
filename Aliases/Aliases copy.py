import csv
import clr
import sys
import System
import time
import argparse
import shutil
import logging
from System.Collections import *

sys.path.append("c:\\Program Files\\National Instruments\\VeriStand 2023\\nivs.lib\\Reference Assemblies")
clr.AddReference("NationalInstruments.VeriStand.SystemDefinitionAPI")
clr.AddReference("NationalInstruments.VeriStand.ClientAPI")
clr.AddReference("NationalInstruments.VeriStand")

from NationalInstruments.VeriStand.SystemDefinitionAPI import SystemDefinition, Alias
from NationalInstruments.VeriStand.ClientAPI import Factory, SystemState
from NationalInstruments.VeriStand import Error


# See http://pythonnet.github.io/ for PyhtonNet documentation

# Open reference to SystemDefinition

    # systemDefinitionFilePath = r"C:\Users\dsamuels\Documents\VeriStand Projects\Engine Demo 2\Engine Demo.nivssdf"
    # systemDefinitionObject = SystemDefinition(systemDefinitionFilePath)

    # channelPathSources = System.Array[System.String]([])
    # channelPathDestinations = System.Array[System.String]([])
    # channelPathSources_returned = System.Array[System.String]([])
    # channelPathDestinations_returned = System.Array[System.String]([])

# GetChannelMappings, Read current mapped signals

    # functionReturn,channelPathSources_returned,channelPathDestinations_returned  = systemDefinitionObject.Root.GetChannelMappings(channelPathSources,channelPathDestinations)

# for i in channelPathSources_returned:
#     print("channelPathSources_returned: ",i)
# for i in channelPathDestinations_returned:
#     print("channelPathDestinations_returned: ",i)

# def ImportMappingsFile():
    # Return object? return error ? Docstring?
    # count = 0
    # try:
    #     with open("dummy_export.txt") as file:
    #         fileContent = file.readlines()
    #         for line in fileContent:
    #             count += 1
    #             print("Line{}: {}".format(count,line.strip()))
    # except IOError as e:
    #     print(e)
class AliasController:
    def __init__(self):
        self._system_definition_object = None
        self._first_target = None

    def create_system_definition(self,ip_address_in,data_rate_in):
        """
        Create a system definition and set properties.
        """
        logging.info("Creating System Definition")
        name = System.String("Name")
        description = System.String("Description")
        creator = System.String("Creator")
        version = System.String("1")
        target_name = System.String("MyController")
        target_type = System.String("Linux_x64")
        filepath = System.String(os.path.join(build_dir, "apadef.nivssdf"))
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
# def GetColumnsFromMappingsFile(mappingsFile = "dummy_export.txt"):
#     count = 0
#     source = []
#     destination = []
#     error = ""
#     try:
#         with open(mappingsFile) as file:
#             fileContent = csv.reader(file, delimiter='\t')
#             for content in fileContent:
#                 source.append(content[0])
#                 destination.append(content[1])
#             print("Source and dest read")
#             return source, destination, error
#     except IOError as e:
#         print(e)
#         return source, destination, e

# def AppendLineToMappingsFile(source, dest):
    # '''
    # Append source and dest paths to next row in Alias mapping file.

    #         Parameters:
    #                 a (str): path of source
    #                 b (str): alias path
    # '''
    # rows = zip(source,dest)
    # try:
    #     with open('dummy_export.txt','a', newline='') as file:
    #         writer = csv.writer(file, delimiter="\t")
    #         for row in rows:
    #             writer.writerow(row)
    # except IOError as e:
    #     print(e)

# def AppendMappingPointToSystemDefinition(source, destination):
#     '''
#     Write source and destination point into the systemDefinition file.

#             Parameters:
#                     a (str): source path
#                     b (str): destination path (or alias path)
#     '''
#     source_ = []
#     destination_ = []
#     error_ = Error()

#     source_.append(source)
#     destination_.append(destination)
#     functionReturn, error_out = systemDefinitionObject.Root.AddChannelMappings(source_,destination_,error_)
#     print(functionReturn,error_out)
#     print("Datapoint written to systemdefinitionfile")

# def WriteMappingsFileToSystemDefinition(mappingsFile):
#     '''
#     Write data from Mappings file into systemDefinition file.

#             Parameters:
#                     a (str): path of Mappings text file
#     '''
#     source, destination, error1 = GetColumnsFromMappingsFile(mappingsFile)
#     error_ = Error()
#     functionReturn, error_out = systemDefinitionObject.Root.AddChannelMappings(source,destination,error_)

#     print("Mappings file written to systemdefinitionfile")

    def SaveSystemDefinition():
        # Save SystemDefinitionFile
        error = System.String("")
        error_out = System.String("")
        functionReturn, error_out = self._system_definition_object.SaveSystemDefinitionFile(error)

        if (not error_out):
            print("File saved")
        else:
            print(error_out)

# MAIN

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='SysDef to be processed')
    parser.add_argument('--SysDef',
                        metavar='FILE_PATH',
                        type=str,
                        action='store',
                        help='Path+name of file to append to')
    args = parser.parse_args()

    dst = r"C:\Users\User\Documents\VeriStand Projects\Test\Test_copy.nivssdf"
    shutil.copyfile(args.SysDef, dst)
    print("Copied file: {}".format(dst), "\n")

    print("inputted file: {}".format(args.SysDef), "\n")
    # C:\Users\User\Documents\VeriStand Projects\Test
