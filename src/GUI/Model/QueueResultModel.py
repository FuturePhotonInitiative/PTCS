import datetime
import json


class QueueResultsModel:
    def __init__(self,
                 start_datetime=datetime.datetime.today(),
                 end_datetime=datetime.datetime.today(),
                 experiments_results_locations=None,
                 queue_result_config=None):
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


    def add_experiment_result(self,
                              experiment_config_location):
        self.experiments_results_locations.append(experiment_config_location)

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