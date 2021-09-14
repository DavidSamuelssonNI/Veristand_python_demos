import csv
import clr
import sys
import System
import time
from System.Collections import *

sys.path.append("c:\\Program Files (x86)\\National Instruments\\VeriStand 2020\\nivs.lib\\Reference Assemblies")
clr.AddReference("NationalInstruments.VeriStand.SystemDefinitionAPI")
clr.AddReference("NationalInstruments.VeriStand.ClientAPI")
clr.AddReference("NationalInstruments.VeriStand")

from NationalInstruments.VeriStand.SystemDefinitionAPI import SystemDefinition, Alias
from NationalInstruments.VeriStand.ClientAPI import Factory, SystemState
from NationalInstruments.VeriStand import Error

# Open reference to SystemDefinition

systemDefinitionFilePath = r"C:\Users\dsamuels\Documents\VeriStand Projects\Engine Demo 20\Engine Demo.nivssdf"
systemDefinitionObject = SystemDefinition(systemDefinitionFilePath)

channelPathSources = System.Array[System.String]([])
channelPathDestinations = System.Array[System.String]([])
channelPathSources_returned = System.Array[System.String]([])
channelPathDestinations_returned = System.Array[System.String]([])

# GetChannelMappings, Read current mapped signals

IronPythonPlaceHolder,channelPathSources_returned,channelPathDestinations_returned  = systemDefinitionObject.Root.GetChannelMappings(channelPathSources,channelPathDestinations)

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

def GetColumnsFromMappingsFile(mappingsFile = "dummy_export.txt"):
    count = 0
    source = []
    destination = []
    error = ""
    try:
        with open(mappingsFile) as file:
            fileContent = csv.reader(file, delimiter='\t')
            for content in fileContent:
                source.append(content[0])
                destination.append(content[1])
            print("Source and dest read")
            return source, destination, error
    except IOError as e:
        print(e)
        return source, destination, e

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

def AppendMappingPointToSystemDefinition(source, destination):
    '''
    Write source and destination point into the systemDefinition file.

            Parameters:
                    a (str): source path
                    b (str): destination path (or alias path)
    '''
    source_ = []
    destination_ = []
    error_ = Error()

    source_.append(source)
    destination_.append(destination)
    IronPythonPlaceHolder, error_out = systemDefinitionObject.Root.AddChannelMappings(source_,destination_,error_)
    print(IronPythonPlaceHolder,error_out)
    print("Datapoint written to systemdefinitionfile")

def WriteMappingsFileToSystemDefinition(mappingsFile):
    '''
    Write data from Mappings file into systemDefinition file.

            Parameters:
                    a (str): path of Mappings text file
    '''
    source, destination, error1 = GetColumnsFromMappingsFile(mappingsFile)
    error_ = Error()
    IronPythonPlaceHolder, error_out = systemDefinitionObject.Root.AddChannelMappings(source,destination,error_)

    print("Mappings file written to systemdefinitionfile")

def SaveSystemDefinition():
    # Save SystemDefinitionFile
    error = System.String("")
    error_out = System.String("")
    IronPythonPlaceHolder, error_out = systemDefinitionObject.SaveSystemDefinitionFile(error)

    if (not error_out):
        print("File saved")
    else:
        print(error_out)

# MAIN
if __name__ == "__main__":
    testSource = "Targets/Controller/System Channels/Absolute Time"
    testDestination = "Targets/Controller/System Channels/System Command"


    AppendMappingPointToSystemDefinition(testSource,testDestination)
    #WriteMappingsFileToSystemDefinition("export_example.txt")
    SaveSystemDefinition()
