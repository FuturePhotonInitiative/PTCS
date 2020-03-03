import sys
import contextlib2
import importlib

from src.GUI.RunAConfigFile.Args import Args
from src.GUI.RunAConfigFile.DeviceSetup import DeviceSetup
from src.GUI.Model.ConfigFile import ConfigFile
from src.GUI.Util.CONSTANTS import CONFIG_SCHEMA_FILE_NAME


def spawn_scripts(scripts, data_map, experiment_result):
    """
    Runs the scripts defined in the JSON config. The tasks are called based on the order specified in the config,
        two different tasks can have the same order, meaning they should be spawned at the same time.
    :param scripts: The scripts pulled from the config
    :param data_map: The dictionary to store data between tasks
    :param experiment_result: The experiment result object to pass into the main class of the script(s) when called
    :return: None
    """
    for script in scripts:
        file_name = script.source[:-3]
        file_module_name = "src.Scripts." + file_name

        script_module = __import__(file_module_name, fromlist=["main"])
        if file_module_name in sys.modules:
            script_module = importlib.reload(script_module)

        script_main_func = getattr(script_module, "main")
        script_main_func(data_map, experiment_result)

    print("Scripts Completed")
    return


def main(args, config_manager=None, queue_result=None):
    """
    Entry point of PTCS.
    Loads config file, parses parameters, sets up the devices, and runs the scripts specified.
    :param args: run RunAConfigFileMain.py with no arguments to see the argument specification
    :param config_manager: the ConfigurationManager object to obtain configuration data for running the scripts
    :param queue_result: the QueueResult object to add run result data to
    :return: None
    """
    from .Application.SystemConfigManager import SystemConfigManager
    if config_manager is None:
        config_manager = SystemConfigManager()
    results_manager = config_manager.get_results_manager()

    from .Model.QueueResultModel import QueueResultsModel
    if queue_result is None:
        queue_result = QueueResultsModel()

    print('Starting PTCS...')

    arguments = Args()
    arguments.parse(args[1:])
    file_name = arguments.obtain_config_file()
    if not file_name:
        print('Goodbye')
        sys.exit(1)

    config = ConfigFile.from_json_file(file_name, CONFIG_SCHEMA_FILE_NAME)

    data_map = {'Data': {}, 'Config': config.to_dict()}

    """
    Argument location precedence:
    First the arguments are read from the data section of the experiment json file
    Then, if one is provided, arguments are read from the parameter file
    Finally, arguments explicitly defined on the command line are added
    Arguments added later may override ones added previously if they have the same name
    """
    config.initialize_data(data_map)
    arguments.add_parameters(data_map)

    print(("Running Experiment: " + config.name + "\n\n"))
    experiment_result, experiment_result_name = \
        results_manager.make_new_experiment_result(file_name, queue_result)

    with contextlib2.ExitStack() as stack:
        # if there are devices in the config file
        if config.devices:
            device_setup = DeviceSetup()
            data_map['Devices'] = device_setup.connect_devices(config.devices, stack)

        # save the config and the param file to the results directory
        experiment_result.add_json_file_dict("Config", data_map['Config'])
        if arguments.get_param_file():
            experiment_result.add_result_file(arguments.get_param_file())
        spawn_scripts(config.experiment, data_map, experiment_result)

    experiment_result.end_experiment()
    results_manager.save_experiment_result(experiment_result_name, experiment_result)
    print('Experiment complete, goodbye!')
