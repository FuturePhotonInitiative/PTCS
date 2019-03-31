import datetime
import os

from src.GUI.Model import QueueResultModel
from src.GUI.Model.ExperimentResultModel import ExperimentResultsModel

QUEUE_FILE_TITLE = "queue_result"
EXPERIMENT_FILE_TITLE = "experiment_result"

class ResultsManager:
    def __init__(self, results_root, results_config_root):
        self.results_root = results_root
        self.results_config_root = results_config_root
        self.queue_result_list = []
        self.experiment_result_list = {}
        for config in os.listdir(results_config_root):
            if QUEUE_FILE_TITLE in config:
                self.queue_result_list.append(QueueResultModel.QueueResultsModel(queue_result_config=config))
            else:
                self.experiment_result_list[config] = (ExperimentResultsModel(results_root,
                                                                              experiment_result_config=config))


    def get_list_of_queue_results(self):
        pass

    def make_new_experiment_result(self, exeriment_config_location):
        now = datetime.datetime.today()
        name = EXPERIMENT_FILE_TITLE + str(now)
        os.mkdir(self.results_root + "\\" + name)
        result = ExperimentResultsModel(self.results_root + "\\" + name, exeriment_config_location)
        result.set_start(now)
        self.experiment_result_list[name] = result
        return [result, name]