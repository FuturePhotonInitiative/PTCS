import inspect
import json
import sys
import types
import pyvisa
import os
import contextlib2
import imp

from Probe.Args import Args
from Probe.ConfigFileManipulation import ConfigFileManipulation

instruments = None


def attach_VISA(manager, name, default):
    """
    Attaches device in VISA format, will scan for devices once because it is a slow process, caches results for future
        use. This will attempt to connect to a default address if it is specified in the JSON config, otherwise it will
        prompt the user to input an address from the list of currently connected devices.
    :param manager: A pyVISA resource manager
    :param name: The name of the device being connected
    :param default: The default address to connect to or None
    :return: A pyVISA device
    """
    global instruments
    if instruments is None:
        instruments = manager.list_resources_info()

    if default:
        for item in instruments.values():
            if str(item.resource_name) == default or item.alias is not None and str(item.alias) == default:
                return manager.open_resource(default)
        print("The default port " + default + " for " + name + " could not be found, please select it manually")
    else:
        print("The default port for " + name + " was not specified, please choose one manually")

    print("*****Connected Devices*****")
    for item in instruments.values():
        line = item.resource_name
        if item.alias is not None:
            line += " -> '" + item.alias + "'"
        print(line)
    print("***************************")
    instr = raw_input("Choose instrument to connect to: ")
    return manager.open_resource(instr)


def connect_devices(config_file, file_locations, exit_stack):
    """
    Initializes all devices specified in the JSON config, this will also dynamically import the drivers specified if one
        hasn't been imported already
    :param config_file: The JSON config object
    :param file_locations: The JSON Files object with standard file directories
    :param exit_stack: A Exit Stack that will close all devices when the program exits
    :return: A dict of device names mapping to their objects
    """
    manager = pyvisa.ResourceManager()
    driver_root = str(file_locations['Driver_Root'])
    drivers = os.listdir(driver_root)
    drivers = [i[:-3] for i in drivers if not (i == '__init__.py' or i[-3:] != '.py')]
    devices = {}

    print "Finding Devices...."

    with open(file_locations["Hardware_Config"]) as d:
        hardware_manager = json.load(d)
    # this one is updated for the hardware manager
    for dev in config_file['Devices']:
        if dev not in hardware_manager.keys():
            print "Device not found in Devices.json: "+dev
        else:
            connection = None
            device = hardware_manager[dev]
            print device
            if str(device['Type']) == "VISA":
                connection = attach_VISA(manager, str(dev), str(device['Default']))
            elif str(device['Type']) == "DIRECT" and "Default" in device.keys():
                connection = str(device['Default'])
            else:
                connection = raw_input(
                    "\'" + str(dev) + "\' cannot be used with VISA, Please enter connection info (eg. IP address): ")

            driver = str(device['Driver'])
            if driver in drivers:
                if driver not in [i[0] for i in globals().items() if isinstance(i[1], types.ModuleType)]:
                    globals()[driver] = imp.load_source(driver, driver_root + '\\' + driver + '.py')
                devices[str(dev)] = exit_stack.enter_context(inspect.getmembers(globals()[driver],
                                                                                inspect.isclass)[0][1](connection))
            else:
                sys.exit("Driver file for \'" + driver + "\' not found in Driver Root: \'" + driver_root)
    return devices


def spawn_scripts(scripts, data_map, json_locations, experiment_result):
    """
    Runs the scripts defined in the JSON config. The tasks are called based on the order specified in the config,
        two different tasks can have the same order, meaning they should be spawned at the same time.
    :param scripts: The scripts pulled from the config
    :param data_map: The dictionary to store data between tasks
    :param json_locations: The JSON Files object with standard file directories
    :return: None
    """
    script_root = str(json_locations['Script_Root'])
    # if script_root[0] is '.':
    #     script_root = os.path.join(os.path.dirname(__file__), script_root)

    for frame in scripts:
        threads = []
        for task in frame:  # todo # dd Multi-Threading support here
            module = str(task)[:-3]
            if module not in [i[0] for i in globals().items() if isinstance(i[1], types.ModuleType)]:
                print script_root + '\\' + module + '.py'
                globals()[module] = imp.load_source(module, script_root + '\\' + module + '.py')
            [i[1] for i in inspect.getmembers(globals()[module], inspect.isfunction) if i[0] is 'main'][0](data_map, experiment_result)
    print "Scripts Completed"
    return


def main(args, config_manager=None, queue_result=None, logger = None):
    """
    Entry point of SPAE, loads config file
    :param args: test configuration file
    :return: None
    """
    from GUI.Application.SystemConfigManager import SystemConfigManager
    if config_manager is None:
        config_manager = SystemConfigManager('../System/Files.json')

    print('Starting SPAE...')

    arguments = Args()
    arguments.parse(args[1:])
    file_name = arguments.obtain_config_file()
    if not file_name:
        print('Goodbye')
        sys.exit(1)

    config = ConfigFileManipulation(file_name)
    config.check_validity(config_manager.file_locations)

    data_map = {'Data': {}, 'Config': config.config}

    """
    Argument location precedence:
    First the arguments are read from the data section of the experiment json file
    Then, if one is provided, arguments are read from the parameter file
    Finally, arguments explicitly defined on the command line are added
    Arguments added later may override ones added previously if they have the same name
    """
    config.initialize_data(data_map)
    arguments.add_parameters(data_map)

    print("Running Experiment: " + config.config['Name'] + "\n\n")
    experiment_result, experiment_result_name = \
        config_manager.get_results_manager().make_new_experiment_result(file_name, queue_result)

    scripts = config.extract_scripts(config_manager.file_locations)

    # autocloses devices if an error occurred
    with contextlib2.ExitStack() as stack:
        data_map['Devices'] = connect_devices(config.config, config_manager.file_locations, stack)
        spawn_scripts(scripts, data_map, config_manager.file_locations, experiment_result)

    experiment_result.end_experiment()
    config_manager.get_results_manager().save_experiment_result(experiment_result_name, experiment_result)
    print 'Experiment complete, goodbye!'


if __name__ == '__main__':
    main(sys.argv)
