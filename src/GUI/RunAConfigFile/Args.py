import argparse
import re


class Args:

    def __init__(self):
        parser = argparse.ArgumentParser(description="Run an Experiment")
        parser.add_argument("-c", "--configFile",
                            help="configuration json file")
        parser.add_argument("-p", "--paramFile", type=argparse.FileType('r'),
                            help="parameter .txt file")
        parser.add_argument("additionalParams", nargs='*',
                            help="additional configuration data is able to be"
                                 " specified in the form \"variable=value\"")

        self.parser = parser
        self.parsed = None
        self.parameters = None

    def parse(self, args):
        self.parsed = self.parser.parse_args(args)
        acquired_parameters = []
        if self.parsed.paramFile:
            acquired_parameters.extend(self.parse_parameter_file(self.parsed.paramFile))
        if self.parsed.additionalParams:
            acquired_parameters.extend(self.parsed.additionalParams)
        self.parameters = self.parse_command_line_definitions(acquired_parameters)

    @staticmethod
    def parse_parameter_file(arg_file):
        """
        Creates a list of arguments to be parsed in the same way as command line arguments from a parameter file
        :param arg_file:
            file object representing the parameter file
        :return:
            A list of arguments from the parameter file in the format defined for command line variable definition
        """
        arg_list = []
        contents = arg_file.read()
        # One variable per line in this format
        for line in contents.split("\n"):
            # The variable name immediately follows a java comment
            tmp = line.split("//")
            if re.match("^\".*\"$", tmp[0]) is None:
                args = tmp[0].split(" ")
            else:
                args = [tmp[0]]
            for i in range(len(args)):
                args[i] = args[i].strip()
            # Ada comments define actual comments
            name = tmp[1].split("--")[0].strip()
            # Remove things that weren't really arguments from the list (generally caused by whitespace)
            args = filter(lambda arg: len(arg) > 0, args)
            # Only return the to string of the list if there's more than one element
            if len(args) >= 2:
                arg_list.append(name + "=" + str(args))
            else:
                arg_list.append(name + "=" + str(args[0]))
        return arg_list

    @staticmethod
    def parse_command_line_definitions(args):
        """
        Parses experiment parameters provided at the command line and adds them to the data dictionary.
        :param args:
            The argument list, not including the program name (sys.argv[0]), the json config file, or the param file.
            It is recommended to call this using python list slicing (sys.argv[2:]).
        :return:
            A list of variable=value definitions
        """
        return_lst = []
        for var in args:
            # If the user quoted the entire option string
            if re.match(r"^\".*\"$", var) and (re.match(r"^\"[^\"]*\"=\"[^\"]*\"$", var) is None):
                # Strip the outermost quotes
                var = var[1:-1]
            variable = re.split("=", var)
            # If the user quoted the variable name
            if re.match(r'^\".*\"$', variable[0]):
                # Strip the quotes around the variable name
                variable[0] = variable[0].strip('"')
            # Handle list parsing
            if re.match(r'^\[.*\]$', variable[1]):
                variable[1] = variable[1].strip(r"\[\]")
                variable[1] = variable[1].split(',')
            # Match numbers and convert them into floats, otherwise leave the input alone
            # (No, we don't yet handle lists or objects, even though they're both valid JSON types)
            # Note: if the user quoted the variable value, it will always be treated as a string, even if it only consists
            # of numerical characters
            if type(variable[1]) is list:
                for i in range(len(variable[1])):
                    # This allows numbers to be quoted because that's how python represents strings in a list when it
                    # stringifies the list, and that only happens when we read from the parameters.txt file
                    # Python also adds spaces in the strinigification of lists, so we need to allow those through and then
                    # strip them as well
                    if re.match(r'^\s*["\']?[0-9]*\.?[0-9]*["\']?\s*$', variable[1][i]):
                        variable[1][i] = variable[1][i].strip(" \t\'\"")
                        variable[1][i] = float(variable[1][i])
            else:
                if re.match(r'^[0-9]*\.?[0-9]*$', variable[1]):
                    variable[1] = float(variable[1])
            return_lst.append(variable)
        return return_lst

    def add_parameters(self, data_map):
        for item in self.parameters:
            # The config data is stored in two places in the data map
            data_map['Config']["data"][item[0]] = item[1]
            data_map['Data']['Initial'][item[0]] = item[1]

    def obtain_config_file(self):
        """
        allows for the input of an experimental config file if no config
        file was supplied in the arguments
        :return: the config file name
        """
        if self.parsed.configFile is None:
            return raw_input("Enter config file name or nothing to exit: ")
        return self.parsed.configFile

    def get_param_file(self):
        return self.parsed.paramFile.name if self.parsed.paramFile else None
