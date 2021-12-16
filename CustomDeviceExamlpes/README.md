# CarMaker custom device add channel Example

This example automatically adds channels to a CarMaker custom device.

In contrast to the standard components of the SystemDefinition. The Custom Devices components are identified using NodeID's and GUID for their graphical components (like the Inputs directory). These identifiers are used by the example to be able to write new channel items to the custom device.

Output example:

<img src="https://user-images.githubusercontent.com/86668144/146374910-da75b50c-c773-4ae2-aa56-8f21995770b7.png" alt="drawing" width="200"/>

## Prerequsite:

The example assumes that the project contains a CarMaker custom device. And that you add a path to your SystemDefinition file instead of:
> systemDefinitionFilePath = r"C:\Users\dsamuels\Documents\VeriStand Projects\Engine Demo 26\Engine Demo.nivssdf"

## How to run

Run the example by execute (tested on python 3.7):
> py -3.7 .\customDeviceAddSignalExample.py

## Clarification

- NodeID

    The customdevice and its components has a unique NodeID. The example reads CarMaker's id in the given systemdefinition file.

- CustomDevice class

    The CustomDevice class is used to read the custom device section's NodeID

- CustomDeviceSection

    The CustomDeviceSection class is used to get the number of channels of the current custom device and the GUID of the section (for example the GUID and nr of channels of the Inputs folder in CarMakers custom device).

- GUID

    A string containing a reference to the graphica object seen in Veristand (for example the Inputs directory).

## TODO

Make more generic, create Custom Device if it doesnt exist and so on...
