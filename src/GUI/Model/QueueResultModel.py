import datetime
import json

from src.GUI.Util.Functions import clean_name_for_file
from src.GUI.Util.GUI_CONSTANTS import QUEUE_FILE_TITLE


class QueueResultsModel:
    def __init__(self,
                 results_config_root,
                 start_datetime=datetime.datetime.today(),
                 end_datetime=datetime.datetime.today(),
                 experiments_results_locations=None,
                 queue_result_config=None):
        self.results_config_root = results_config_root
        if queue_result_config is None:
            if experiments_results_locations is None:
                experiments_results_locations = []
            self.start_datetime = start_datetime
            self.end_datetime = end_datetime
            self.experiments_results_locations = experiments_results_locations
        else:
            self.load_from_json(queue_result_config)

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
        config_dict = json.load(open(filename))
        self.start_datetime = datetime.datetime.strptime(config_dict["start_datetime"], '%Y-%m-%d %H:%M:%S.%f')
        self.end_datetime = datetime.datetime.strptime(config_dict["end_datetime"], '%Y-%m-%d %H:%M:%S.%f')
        self.experiments_results_locations = config_dict["experiments_results_locations"]

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
        config_dict["end_datetime"] = self.end_datetime
        config_dict["start_datetime"] = self.start_datetime
        config_dict["experiments_results_locations"] = self.experiments_results_locations
        with open(filename, 'w') as config_file:
            json.dump(config_dict, config_file, indent=4 if pretty_print else None, default=str)

    def save(self):
        self.export_to_json(self.results_config_root + "/" + self.get_name() + ".json")

    def get_name(self):
        now = self.start_datetime
        name = QUEUE_FILE_TITLE + str(now)
        name = clean_name_for_file(name)
        return name

    def add_experiment_result(self,
                              experiment_result_location):
        self.experiments_results_locations.append(experiment_result_location)

    def start_queue(self):
        self.start_datetime = datetime.datetime.today()

    def end_queue(self):
        self.end_datetime = datetime.datetime.today()

    def set_start(self, start_datetime):
        self.start_datetime = start_datetime

    def set_end(self, end_datetime):
        self.end_datetime = end_datetime

    def get_experiment_results_list(self):
        return self.experiments_results_locations