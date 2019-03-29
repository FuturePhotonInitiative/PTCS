import datetime
import json
import os
from shutil import copyfile


class ExperimentResultsModel:
    def __init__(self,
                 experiment_results_directory,
                 experiment_config_location,
                 experiments_results_files=None,
                 start_datetime=datetime.datetime.today(),
                 end_datetime=datetime.datetime.today()):
        self.experiment_results_directory = experiment_results_directory
        self.experiment_config_location = json.load(experiment_config_location)
        if experiments_results_files is None:
            experiments_results_files = []
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.experiments_results_files = experiments_results_files

    def load_from_json(self, filename):
        """
        Write the configuration stored in this Experiment object to a json formatted file
        :param filename:
            The name of the file to write to.  WARNING: The specified file will be overwritten
        :param pretty_print:
            If true, print the json with indentation, otherwise keep the JSON compact
        :return:
        None
        """
        config_dict = json.load(filename)
        self.experiment_results_directory = config_dict["experiment_results_directory"]
        self.experiment_config_location = config_dict["experiment_config_location"]
        self.start_datetime = config_dict["start_datetime"]
        self.end_datetime = config_dict["end_datetime"]
        self.experiments_results_files = config_dict["experiments_results_files"]

    def export_to_json(self, filename, pretty_print=True):
        """
        Write the configuration stored in this Experiment object to a json formatted file
        :param filename:
            The name of the file to write to.  WARNING: The specified file will be overwritten
        :param pretty_print:
            If true, print the json with indentation, otherwise keep the JSON compact
        :return:
        None
        """
        config_dict = {}
        config_dict["experiment_results_directory"] = self.experiment_results_directory
        config_dict["experiment_config_location"] = self.experiment_config_location
        config_dict["start_datetime"] = self.start_datetime
        config_dict["end_datetime"] = self.end_datetime
        config_dict["experiments_results_files"] = self.experiments_results_files

        with open(filename, 'w') as config_file:
            json.dump(config_dict, config_file, indent=4 if pretty_print else None)

    def add_result_file(self, experiment_file_location):
        path_of_file = os.path.dirname(file)
        if path_of_file != self.experiment_results_directory:
            file_name = experiment_file_location.replace(path_of_file, "")
            copyfile(experiment_file_location, self.experiment_results_directory + file_name)
            self.experiments_results_files.append(self.experiment_results_directory + file_name)
        else:
            self.experiments_results_files.append(experiment_file_location)

    def start_experiment(self):
        self.start_datetime = datetime.datetime.today()

    def end_experiment(self):
        self.end_datetime = datetime.datetime.today()

    def set_experiment(self, start_datetime):
        self.start_datetime = start_datetime

    def set_end(self, end_datetime):
        self.end_datetime = end_datetime

    def get_experiment_results_file_list(self):
        return self.experiments_results_files