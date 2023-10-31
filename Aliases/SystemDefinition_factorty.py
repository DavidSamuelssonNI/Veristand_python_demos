
import sys
import os
# directory reach
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
build_dir = os.path.abspath(os.path.join(parent_dir, 'build'))
bin_dir = os.path.abspath(os.path.join(parent_dir, 'bin'))
sys.path.append(parent_dir)
try:
    os.mkdir(build_dir)
except Exception:
    pass
import logging
import lib._internal
import argparse
import pathlib
import System # noqa
from System.Collections import * # noqa

from NationalInstruments.VeriStand.SystemDefinitionAPI import \
     SystemDefinition, Model, NodeIDUtil # noqa
from NationalInstruments.VeriStand.ClientAPI import Factory
from NationalInstruments.VeriStand import Error # noqa

class ProjectFactory:
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


    def AddModel(self, model_path):  # add str as input to choose model to add
        """Add/Append model to System definition file

        Args:
            model_path (str): Path to model binary file

        Returns:
            bool: Model loaded
        """
        print("Path to lib: ", model_path)
        model_error = Error()
        model_added = None
        model_name = System.String(pathlib.Path(model_path).stem)
        model_desc = System.String("")
        model_path = model_path
        processor = System.Int32(0)
        decimation = System.Int32(1)
        initial_state = System.UInt16(0)
        segments_vectors = System.Boolean(False)
        import_parameters = System.Boolean(True)
        import_signals = System.Boolean(True)
        # Create a model object
        my_new_model = Model(model_name,
                             model_desc,
                             model_path,
                             processor,
                             decimation,
                             initial_state,
                             segments_vectors,
                             import_parameters,
                             import_signals)

        self._models_selection = (self._first_target.GetSimulationModels().
                                      GetModels())
        # Add models to project
        [model_added, model_error] = (self._models_selection.
                                      AddModel(my_new_model, model_error))
        self.SaveSystemDefinition()
        print("Model written ok")
        return model_added

    def Deploy(self):
        """Deploy the system definition file
        """
        filepath  = System.String("c:\\Temp\\apadef.nivssdf")
        self.error_check_ = Error()
        self.factory_ = Factory()
        try:
            self.factory_workspace_interface_ = (Factory().
                                                 GetIWorkspace2('localhost'))
        except Exception as e:
            print(e)
        self.system_definition_path = filepath
        print("Deploying")
        deploy_system_definition = System.Boolean(True)
        timeout = System.UInt32(500000)
        self.error_check_ = (self.factory_workspace_interface_.
                             ConnectToSystem(self.system_definition_path,
                                             deploy_system_definition,
                                             timeout))
        print("Project Deployed", "error: ", self.error_check_.
              ResolvedErrorMessage)

    def SaveSystemDefinition(self, save_to_file=""):
        """Save system definition file

        Args:
            save_to_file (str, optional): Choose path+file to write to.
            Defaults to "Overwriting current system def file".

        Returns:
            Boolean: True if saved correctly
        """
        error = System.String("")
        error_out = System.String("")
        if not save_to_file:
            file_saved, error_out = self._system_definition_object. \
                SaveSystemDefinitionFile(error)
        else:
            file_saved, error_out = self._system_definition_object. \
                SaveSystemDefinitionFile(save_to_file, error)

        if (not error_out):
            print("File saved")
            return file_saved
        else:
            print(error_out)

if __name__ == "__main__":
    model_path = str(pathlib.Path(pathlib.Path.cwd().parent,
                                 'bin',
                                 'libengine.so'))
    print(model_path)
    # pf.Deploy()

    parser = argparse.ArgumentParser(description='SysDef to be processed')
    parser.add_argument('--ip_address',
                        metavar='ip_address',
                        type=str,
                        action='store',
                        help='The ip_address of the Real-time system')
    parser.add_argument('--data_rate',
                        metavar='data_rate',
                        type=int,
                        action='store',
                        help='Data rate of Real-time system')
    args = parser.parse_args()

    pf = ProjectFactory()
    pf.create_system_definition(args.ip_address, args.data_rate)
    pf.AddModel(model_path)

    # print("inputted file: {}".format(args.ip_address), "\n")

#VeriStand.exe -sysDef "c:\Temp\apadef.nivssdf" -openProject "c:\Temp\Training1"