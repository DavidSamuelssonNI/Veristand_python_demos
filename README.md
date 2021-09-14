# Veristand_python_demos

## Rewritten Python Demos from "NI Veristand .NET API".
Written for Veristand 2020 but could be rewritten to work with other Veristand Versions.

### **Deploy.py** - Example code to deploy a project in Veristand, using the built-in Engine demo.

* To run the demo
  
  * Set the variable SystemDefinitionFilePath to your project path:  
    Example: System.String("C:\\Users\\dsamuels\\Documents\\VeriStand Projects\\Engine Demo nr\\Engine Demo.nivssdf")
  * Run the Script:  
    Example, using pyton 3.7:`py -3.7 .\Deploy.py`
  
 *Inspired by the example C# Walkthrough: Opening and Running a Project from NI Veristand .NET API documentation*
 
### **SignalMappingsExample.py** - Example code to add signals to mapping list, by exported file or signalwise.

* To run the demo

  * Set the variable SystemDefinitionFilePath to your project path:  
    Example: System.String("C:\\Users\\dsamuels\\Documents\\VeriStand Projects\\Engine Demo nr\\Engine Demo.nivssdf")
  * Use WriteMappingsFileToSystemDefinition("name of file to export signals from.txt") or 
    AppendMappingPointToSystemDefinition(source, destination). The *.txt file should be a tab separated list of 
    source destination
  * Run the Script:
    Example, using python 3.7: `py -3.7 .\SignalMappingsExample.py`
  
 *Inspired by the example: https://knowledge.ni.com/KnowledgeArticleDetails?id=kA00Z0000004AQlSAM* 
  
