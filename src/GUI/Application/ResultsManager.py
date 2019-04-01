import datetime
import os

from src.GUI.Model import QueueResultModel
from src.GUI.Model.ExperimentModel import Experiment
from src.GUI.Model.ExperimentResultModel import ExperimentResultsModel

QUEUE_FILE_TITLE = "queue_result"
EXPERIMENT_FILE_TITLE = "experiment_result"


def clean_name_for_file(name):
    OK_LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"
    name_new = ""
    for letter in name:
        if letter not in OK_LETTERS:
            name_new += "_"
        else:
            name_new += letter
    return name_new


class ResultsManager:
    def __init__(self, results_root, results_config_root):
        self.results_root = results_root
        self.results_config_root = results_config_root
        self.queue_result_list = []
        self.experiment_result_dict = {}
        for config in os.listdir(results_config_root):
            if QUEUE_FILE_TITLE in config:
                self.queue_result_list.append(QueueResultModel.QueueResultsModel(queue_result_config=config))
            else:
                self.experiment_result_dict[config] = (ExperimentResultsModel(results_root,
                                                                              experiment_result_config=results_config_root + "/" + config))


    def get_list_of_queue_results(self):
        pass

    def get_list_of_experiment_result(self, key):
        return self.experiment_result_dict[key]

    def get_list_of_experiment_result_names(self):
        return self.experiment_result_dict.keys()

    def make_new_experiment_result(self, exeriment_config_location):
        now = datetime.datetime.today()
        exp = Experiment(exeriment_config_location)

        name = exp.get_name() + str(now)
        name = clean_name_for_file(name)

        if not os.path.exists(self.results_root):
            os.mkdir(self.results_root)
        if not os.path.exists(self.results_root + "/" + name):
            os.mkdir(self.results_root + "/" + name)

        result = ExperimentResultsModel(self.results_root + "/" + name, exeriment_config_location)
        result.set_start(now)
        self.experiment_result_dict[name] = result
        return [result, name]

    def save_experiment_result(self, name, experiment_result):
        experiment_result.export_to_json(self.results_config_root + "/" + name + ".json")
